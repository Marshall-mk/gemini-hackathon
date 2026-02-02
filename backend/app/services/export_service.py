from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import json
from typing import Dict
from pathlib import Path
import os


class ExportService:
    def __init__(self, output_dir: str = None):
        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir / "data"
        self.output_dir = Path(output_dir) if output_dir else data_dir / "exports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_to_json(self, recipe_data: Dict, recipe_id: int) -> str:
        """Export recipe to JSON file"""
        try:
            filename = f"recipe_{recipe_id}.json"
            filepath = self.output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(recipe_data, f, indent=2, ensure_ascii=False)

            return str(filepath)

        except Exception as e:
            raise Exception(f"Failed to export JSON: {str(e)}")

    def export_to_pdf(self, recipe_data: Dict, recipe_id: int) -> str:
        """Export recipe to PDF file"""
        try:
            filename = f"recipe_{recipe_id}.pdf"
            filepath = self.output_dir / filename

            # Create PDF document
            doc = SimpleDocTemplate(str(filepath), pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)

            # Container for the 'Flowable' objects
            elements = []

            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=30,
                alignment=TA_CENTER
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#34495E'),
                spaceAfter=12,
                spaceBefore=12
            )

            # Title
            title = recipe_data.get('title', 'Untitled Recipe')
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

            # Add thumbnail if available
            if recipe_data.get('thumbnail_path') and os.path.exists(recipe_data['thumbnail_path']):
                try:
                    img = Image(recipe_data['thumbnail_path'], width=4*inch, height=3*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 12))
                except:
                    pass

            # Description
            if recipe_data.get('description'):
                elements.append(Paragraph(recipe_data['description'], styles['Normal']))
                elements.append(Spacer(1, 12))

            # Nutritional Information
            if recipe_data.get('nutrition'):
                elements.append(Paragraph("Nutritional Information", heading_style))
                nutrition = recipe_data['nutrition']

                nutrition_data = []
                if nutrition.get('servings'):
                    nutrition_data.append(['Servings', str(nutrition['servings'])])
                if nutrition.get('calories'):
                    nutrition_data.append(['Calories', f"{nutrition['calories']:.0f} kcal"])
                if nutrition.get('protein'):
                    nutrition_data.append(['Protein', f"{nutrition['protein']:.1f}g"])
                if nutrition.get('carbs'):
                    nutrition_data.append(['Carbohydrates', f"{nutrition['carbs']:.1f}g"])
                if nutrition.get('fats'):
                    nutrition_data.append(['Fats', f"{nutrition['fats']:.1f}g"])
                if nutrition.get('fiber'):
                    nutrition_data.append(['Fiber', f"{nutrition['fiber']:.1f}g"])

                if nutrition_data:
                    nutrition_table = Table(nutrition_data, colWidths=[2*inch, 2*inch])
                    nutrition_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ECF0F1')),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 1, colors.white)
                    ]))
                    elements.append(nutrition_table)
                    elements.append(Spacer(1, 12))

            # Ingredients
            elements.append(Paragraph("Ingredients", heading_style))
            ingredients = recipe_data.get('ingredients', [])

            if ingredients:
                ingredient_items = []
                for ing in ingredients:
                    quantity = ing.get('quantity', '')
                    unit = ing.get('unit', '')
                    name = ing.get('name', '')
                    item_text = f"{quantity} {unit} {name}".strip()
                    ingredient_items.append([Paragraph(f"• {item_text}", styles['Normal'])])

                ingredient_table = Table(ingredient_items, colWidths=[6*inch])
                ingredient_table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(ingredient_table)
                elements.append(Spacer(1, 12))

            # Cooking Steps
            elements.append(Paragraph("Cooking Instructions", heading_style))
            steps = recipe_data.get('steps', [])

            if steps:
                for step in sorted(steps, key=lambda x: x.get('step_number', 0)):
                    step_num = step.get('step_number', 0)
                    instruction = step.get('instruction', '')
                    duration = step.get('duration', '')

                    step_text = f"<b>Step {step_num}:</b> {instruction}"
                    if duration:
                        step_text += f" <i>({duration})</i>"

                    elements.append(Paragraph(step_text, styles['Normal']))
                    elements.append(Spacer(1, 8))

            # Source
            elements.append(Spacer(1, 12))
            if recipe_data.get('video_url'):
                source_text = f"Source: {recipe_data['video_url']}"
                elements.append(Paragraph(source_text, styles['Italic']))

            # Build PDF
            doc.build(elements)

            return str(filepath)

        except Exception as e:
            raise Exception(f"Failed to export PDF: {str(e)}")

    def create_grocery_list_pdf(self, shopping_list: Dict, recipe_title: str) -> str:
        """Create a PDF grocery list"""
        try:
            filename = f"grocery_list_{recipe_title.replace(' ', '_')}.pdf"
            filepath = self.output_dir / filename

            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Title
            title = Paragraph(f"Grocery List: {recipe_title}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))

            # Items
            for item in shopping_list.get('items', []):
                ingredient = item.get('ingredient', '')
                quantity = item.get('quantity', '')

                item_text = f"☐ {ingredient} - {quantity}"
                elements.append(Paragraph(item_text, styles['Normal']))
                elements.append(Spacer(1, 6))

            doc.build(elements)
            return str(filepath)

        except Exception as e:
            raise Exception(f"Failed to create grocery list PDF: {str(e)}")
