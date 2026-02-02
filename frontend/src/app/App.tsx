import { useEffect, useMemo, useState } from "react";
import { Loader2, Send, Key, Brain, Menu, X } from "lucide-react";
import { Input } from "@/app/components/ui/input";
import { Button } from "@/app/components/ui/button";
import { Label } from "@/app/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/app/components/ui/select";
import { Card } from "@/app/components/ui/card";
import { Separator } from "@/app/components/ui/separator";
import { RecipeGallery, type ProcessedVideo } from "@/app/components/RecipeGallery";
import { RecipeDetailDialog } from "@/app/components/RecipeDetailDialog";

// Gemini models available (aligned with backend)
const GEMINI_MODELS = [
  "gemini-3-flash-preview",
  "gemini-3-pro",
];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const API_URL = `${API_BASE_URL}/api`;

type BackendStoreLink = {
  store_name: string;
  search_url: string;
  ingredient: string;
};

type BackendIngredient = {
  id: number;
  name: string;
  quantity?: string | null;
  unit?: string | null;
  store_links?: BackendStoreLink[] | null;
};

type BackendStep = {
  id: number;
  step_number: number;
  instruction: string;
  duration?: string | null;
};

type BackendNutrition = {
  calories?: number | null;
  protein?: number | null;
  carbs?: number | null;
  fats?: number | null;
  fiber?: number | null;
  servings?: number | null;
};

type BackendRecipe = {
  id: number;
  title?: string | null;
  video_url: string;
  platform: string;
  description?: string | null;
  thumbnail_path?: string | null;
  video_path?: string | null;
  created_at: string;
  ingredients?: BackendIngredient[];
  steps?: BackendStep[];
  nutrition?: BackendNutrition | null;
};

type ExtractResponse = {
  success: boolean;
  message: string;
  recipe?: BackendRecipe | null;
};

export default function App() {
  const [apiKey, setApiKey] = useState("");
  const [selectedModel, setSelectedModel] = useState(GEMINI_MODELS[0]);
  const [url, setUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedVideos, setProcessedVideos] = useState<ProcessedVideo[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<ProcessedVideo | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const assetBaseUrl = useMemo(() => API_BASE_URL.replace(/\/$/, ""), []);

  const toPublicAssetPath = (path?: string | null) => {
    if (!path) return "";

    // Step 1: Normalize backslashes to forward slashes (handle Windows paths)
    let normalized = path.replace(/\\/g, "/");

    // Step 2: Remove Windows drive letters (C:/, D:/, etc.) and absolute paths
    normalized = normalized.replace(/^[a-zA-Z]:\//, "");

    // Step 3: Remove leading slashes
    normalized = normalized.replace(/^\/+/, "");

    // Step 4: Handle absolute paths that might contain 'data/' directory
    // Extract everything after '/data/' if present
    if (normalized.includes("/data/")) {
      const parts = normalized.split("/data/");
      if (parts.length > 1) {
        normalized = parts[parts.length - 1];
      }
    }

    // Step 5: Check if already in correct format (images/, videos/, exports/)
    if (normalized.startsWith("images/") ||
        normalized.startsWith("videos/") ||
        normalized.startsWith("exports/")) {
      return normalized;
    }

    // Step 6: Remove data/ prefix if present
    if (normalized.startsWith("data/images/")) return normalized.replace("data/images/", "images/");
    if (normalized.startsWith("data/videos/")) return normalized.replace("data/videos/", "videos/");
    if (normalized.startsWith("data/exports/")) return normalized.replace("data/exports/", "exports/");

    // Step 7: Try to extract directory from path components
    const pathParts = normalized.split("/");
    if (pathParts.includes("images")) {
      const idx = pathParts.indexOf("images");
      return pathParts.slice(idx).join("/");
    }
    if (pathParts.includes("videos")) {
      const idx = pathParts.indexOf("videos");
      return pathParts.slice(idx).join("/");
    }
    if (pathParts.includes("exports")) {
      const idx = pathParts.indexOf("exports");
      return pathParts.slice(idx).join("/");
    }

    // Step 8: Fallback - assume it's an image if it has image extension
    if (/\.(jpg|jpeg|png|gif|webp)$/i.test(normalized)) {
      return `images/${normalized}`;
    }

    // Step 9: Last resort - return as is
    return normalized;
  };

  const mapRecipeToVideo = (recipe: BackendRecipe): ProcessedVideo => {
    const thumbnailPath = toPublicAssetPath(recipe.thumbnail_path);
    const thumbnailUrl = thumbnailPath ? `${assetBaseUrl}/${thumbnailPath}` : "";

    const sortedSteps = [...(recipe.steps ?? [])].sort(
      (a, b) => a.step_number - b.step_number
    );

    const purchaseLinks = (recipe.ingredients ?? []).flatMap((ingredient) => {
      const links = ingredient.store_links ?? [];
      return links.map((link) => ({
        item: `${ingredient.name} · ${link.store_name}`,
        url: link.search_url,
      }));
    });

    return {
      id: String(recipe.id),
      url: recipe.video_url,
      thumbnail: thumbnailUrl || "https://via.placeholder.com/640x360?text=No+Image",
      title: recipe.title || "Untitled Recipe",
      recipes: [
        {
          name: recipe.title || "Untitled Recipe",
          description: recipe.description || "No description available.",
          steps: sortedSteps.map((step) => step.instruction),
          purchaseLinks,
          nutrition: {
            calories: recipe.nutrition?.calories ?? null,
            protein: recipe.nutrition?.protein ?? null,
            carbs: recipe.nutrition?.carbs ?? null,
            fat: recipe.nutrition?.fats ?? null,
            fiber: recipe.nutrition?.fiber ?? null,
          },
        },
      ],
      processedAt: new Date(recipe.created_at),
    };
  };

  const loadRecipes = async () => {
    try {
      setErrorMessage(null);
      const response = await fetch(`${API_URL}/recipes`);
      if (!response.ok) {
        throw new Error("Failed to load recipes");
      }
      const data = (await response.json()) as BackendRecipe[];
      const mapped = data
        .map(mapRecipeToVideo)
        .sort((a, b) => b.processedAt.getTime() - a.processedAt.getTime());
      setProcessedVideos(mapped);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to load recipes";
      setErrorMessage(message);
    }
  };

  useEffect(() => {
    loadRecipes();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url) {
      alert("Please enter a video URL");
      return;
    }

    setIsProcessing(true);

    try {
      setErrorMessage(null);
      const response = await fetch(`${API_URL}/recipes/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          video_url: url,
          model: selectedModel,
        }),
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => null);
        const detail = errorPayload?.detail || "Failed to extract recipe";
        throw new Error(detail);
      }

      const data = (await response.json()) as ExtractResponse;
      if (!data.success || !data.recipe) {
        throw new Error(data.message || "Failed to extract recipe");
      }

      const newVideo = mapRecipeToVideo(data.recipe);
      setProcessedVideos((prev) => [newVideo, ...prev.filter((video) => video.id !== newVideo.id)]);
      setSelectedVideo(newVideo);
      setIsDialogOpen(true);
      setUrl("");
    } catch (error) {
      const message = error instanceof Error ? error.message : "An error occurred";
      setErrorMessage(message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleVideoClick = (video: ProcessedVideo) => {
    setSelectedVideo(video);
    setIsDialogOpen(true);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className={`bg-white border-r border-gray-200 p-6 flex flex-col transition-all duration-300 ${
        isSidebarCollapsed ? 'w-0 p-0 overflow-hidden' : 'w-80'
      }`}>
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-2xl font-bold text-gray-900">Recipe Extractor</h1>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsSidebarCollapsed(true)}
              className="h-8 w-8"
            >
              <X className="size-4" />
            </Button>
          </div>
          <p className="text-sm text-gray-500">Extract recipes from cooking videos using AI</p>
        </div>

        <Separator className="mb-6" />

        <div className="space-y-6 flex-1">
          <div>
            <Label htmlFor="api-key" className="flex items-center gap-2 mb-2">
              <Key className="size-4" />
              API Key
            </Label>
            <Input
              id="api-key"
              type="password"
              placeholder="Enter your Gemini API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="font-mono text-sm"
            />
            <p className="text-xs text-gray-500 mt-2">
              API key is configured on the server. This field is optional.
            </p>
          </div>

          <div>
            <Label htmlFor="model-select" className="flex items-center gap-2 mb-2">
              <Brain className="size-4" />
              Gemini Model
            </Label>
            <Select value={selectedModel} onValueChange={setSelectedModel}>
              <SelectTrigger id="model-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {GEMINI_MODELS.map((model) => (
                  <SelectItem key={model} value={model}>
                    {model}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500 mt-2">
              Choose the AI model for recipe extraction
            </p>
          </div>
        </div>

        <div className="mt-auto pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-400 text-center">
            Powered by Google Gemini AI
          </p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          {/* Toggle Button for collapsed sidebar */}
          {isSidebarCollapsed && (
            <Button
              variant="outline"
              size="icon"
              onClick={() => setIsSidebarCollapsed(false)}
              className="mb-6 h-10 w-10"
            >
              <Menu className="size-5" />
            </Button>
          )}

          {/* URL Input Section */}
          <Card className="p-6 mb-8">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="video-url" className="text-base mb-2 block">
                  Video URL
                </Label>
                <div className="flex gap-3">
                  <Input
                    id="video-url"
                    type="url"
                    placeholder="Paste your YouTube or video URL here..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={isProcessing}
                    className="flex-1"
                  />
                  <Button
                    type="submit"
                    disabled={isProcessing || !url}
                    size="lg"
                    className="min-w-32"
                  >
                    {isProcessing ? (
                      <>
                        <Loader2 className="size-4 mr-2 animate-spin" />
                        Processing
                      </>
                    ) : (
                      <>
                        <Send className="size-4 mr-2" />
                        Extract
                      </>
                    )}
                  </Button>
                </div>
                <p className="text-sm text-gray-500 mt-2">
                  Enter a video URL to extract recipes and cooking instructions
                </p>
                {errorMessage && (
                  <p className="text-sm text-red-600 mt-2">{errorMessage}</p>
                )}
              </div>
            </form>
          </Card>

          {/* Results Gallery */}
          <div>
            <h2 className="text-2xl font-semibold mb-6">Processed Videos</h2>
            <RecipeGallery videos={processedVideos} onVideoClick={handleVideoClick} />
          </div>
        </div>
      </main>

      {/* Recipe Detail Dialog */}
      <RecipeDetailDialog
        video={selectedVideo}
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
      />
    </div>
  );
}