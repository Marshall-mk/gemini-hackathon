from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
from typing import Dict, List, Optional
import cv2
from PIL import Image
import io

load_dotenv()


class GeminiService:
    def __init__(self, model_name: str = 'gemini-3-flash-preview'):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Initialize Gemini 3 client with new SDK
        self.client = genai.Client(api_key=api_key)
        # Support both Gemini 3 Pro and Flash
        self.model_name = model_name

    def analyze_video(self, video_path: str, frames: List = None) -> Dict:
        """
        Analyze cooking video and extract recipe information using Gemini 3
        Returns structured recipe data
        """
        try:
            # Upload video file to Gemini using new SDK
            print(f"Uploading video file: {video_path}")
            video_file = self.client.files.upload(file=video_path)
            print(f"Video uploaded. File ID: {video_file.name}, State: {video_file.state}")

            # Wait for file to be processed and become ACTIVE
            import time
            max_wait = 120  # Maximum 2 minutes wait
            wait_interval = 2  # Check every 2 seconds
            elapsed = 0

            while video_file.state.name != "ACTIVE" and elapsed < max_wait:
                print(f"Waiting for file to be processed... State: {video_file.state.name}")
                time.sleep(wait_interval)
                elapsed += wait_interval
                # Refresh file status
                video_file = self.client.files.get(name=video_file.name)

            if video_file.state.name != "ACTIVE":
                raise Exception(f"Video file did not become ACTIVE within {max_wait} seconds. Current state: {video_file.state.name}")

            print(f"File is now ACTIVE. Proceeding with analysis...")

            prompt = """
            Analyze this cooking video and extract the following information in a structured JSON format:

            {
                "title": "Name of the dish",
                "description": "Brief description of the dish",
                "ingredients": [
                    {
                        "name": "ingredient name",
                        "quantity": "amount",
                        "unit": "measurement unit (e.g., cups, grams, pieces)"
                    }
                ],
                "steps": [
                    {
                        "step_number": 1,
                        "instruction": "Detailed cooking instruction",
                        "duration": "estimated time for this step (e.g., '5 minutes')"
                    }
                ],
                "nutrition": {
                    "calories": estimated_calories_per_serving,
                    "protein": protein_in_grams,
                    "carbs": carbs_in_grams,
                    "fats": fats_in_grams,
                    "fiber": fiber_in_grams,
                    "servings": number_of_servings
                }
            }

            Instructions:
            - Pay attention to both visual cues and any narration/text in the video
            - Extract all ingredients mentioned or shown, with their quantities
            - List cooking steps in chronological order
            - Include estimated time for each step if mentioned or visible
            - Provide nutritional estimates based on the ingredients and portions shown
            - If exact quantities aren't shown, provide reasonable estimates based on what you see
            - If nutritional information cannot be determined, provide null for those fields

            Return ONLY the JSON object, no additional text.
            """

            # Gemini 3 configuration with HIGH thinking level for deep reasoning
            config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=8192,
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.HIGH
                )
            )

            # Generate content using new SDK
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, video_file],
                config=config
            )

            # Parse the JSON response
            recipe_data = self._parse_json_response(response.text)

            return recipe_data

        except Exception as e:
            raise Exception(f"Failed to analyze video with Gemini 3: {str(e)}")

    def analyze_frames(self, frames: List, video_description: str = None) -> Dict:
        """
        Analyze individual frames from video using Gemini 3
        Useful as a fallback or supplement to video analysis
        Uses HIGH media resolution for detailed ingredient identification
        """
        try:
            # Convert frames to image parts
            image_parts = []
            for frame in frames[:5]:  # Use first 5 frames
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                # Convert to bytes
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()

                # Create Part from bytes
                image_part = types.Part.from_bytes(
                    data=img_byte_arr,
                    mime_type='image/jpeg'
                )
                image_parts.append(image_part)

            prompt = """
            Analyze these frames from a cooking video and extract recipe information.
            These frames show different stages of cooking the same dish.

            Extract the following in JSON format:
            {
                "title": "Name of the dish",
                "description": "Brief description",
                "ingredients": [
                    {"name": "ingredient", "quantity": "amount", "unit": "unit"}
                ],
                "steps": [
                    {"step_number": 1, "instruction": "step description", "duration": "time"}
                ],
                "nutrition": {
                    "calories": null,
                    "protein": null,
                    "carbs": null,
                    "fats": null,
                    "fiber": null,
                    "servings": null
                }
            }

            Focus on:
            - Ingredients visible in the frames
            - Cooking techniques and steps shown
            - Any text overlays with ingredient lists or instructions

            Return ONLY the JSON object.
            """

            # Gemini 3 Pro: Use HIGH media resolution for detailed image analysis
            config = types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=8192,
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.HIGH
                ),
                media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH
            )

            # Build contents with images and prompt
            contents = image_parts + [prompt]

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )

            recipe_data = self._parse_json_response(response.text)
            return recipe_data

        except Exception as e:
            raise Exception(f"Failed to analyze frames with Gemini 3: {str(e)}")

    def enhance_recipe_with_nutrition(self, ingredients: List[Dict]) -> Dict:
        """
        Use Gemini 3 to estimate nutritional information based on ingredients
        Uses HIGH thinking level for accurate nutritional calculations
        """
        try:
            ingredients_text = "\n".join([
                f"- {ing['quantity']} {ing.get('unit', '')} {ing['name']}"
                for ing in ingredients
            ])

            prompt = f"""
            Based on these ingredients, estimate the nutritional information per serving:

            Ingredients:
            {ingredients_text}

            Provide the response in JSON format:
            {{
                "calories": estimated_calories_per_serving,
                "protein": protein_in_grams,
                "carbs": carbs_in_grams,
                "fats": fats_in_grams,
                "fiber": fiber_in_grams,
                "servings": estimated_number_of_servings
            }}

            Use standard nutritional data for these ingredients. If you cannot estimate, use null.
            Return ONLY the JSON object.
            """

            # Gemini 3: Use HIGH thinking for precise nutritional calculations
            config = types.GenerateContentConfig(
                temperature=0.5,  # Lower temperature for more precise calculations
                top_p=0.9,
                max_output_tokens=2048,
                thinking_config=types.ThinkingConfig(
                    thinking_level=types.ThinkingLevel.HIGH
                )
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            nutrition_data = self._parse_json_response(response.text)

            return nutrition_data

        except Exception as e:
            print(f"Failed to enhance nutrition data with Gemini 3: {str(e)}")
            return {
                "calories": None,
                "protein": None,
                "carbs": None,
                "fats": None,
                "fiber": None,
                "servings": None
            }

    def _parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON from Gemini response, handling markdown code blocks and thoughts"""
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            # Parse JSON
            data = json.loads(cleaned)
            return data

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {response_text}")
            raise Exception(f"Invalid JSON response from Gemini: {str(e)}")
