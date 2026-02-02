import { PlayCircle } from "lucide-react";
import { Card, CardContent } from "@/app/components/ui/card";

export interface NutritionalInfo {
  calories: number | null;
  protein: number | null; // in grams
  carbs: number | null; // in grams
  fat: number | null; // in grams
  fiber?: number | null; // in grams
  sugar?: number | null; // in grams
  sodium?: number | null; // in mg
}

export interface Recipe {
  name: string;
  description: string;
  steps: string[];
  purchaseLinks: { item: string; url: string }[];
  nutrition: NutritionalInfo;
}

export interface ProcessedVideo {
  id: string;
  url: string;
  thumbnail: string;
  title: string;
  recipes: Recipe[];
  processedAt: Date;
}

interface RecipeGalleryProps {
  videos: ProcessedVideo[];
  onVideoClick: (video: ProcessedVideo) => void;
}

export function RecipeGallery({ videos, onVideoClick }: RecipeGalleryProps) {
  if (videos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <PlayCircle className="size-16 text-gray-300 mb-4" />
        <h3 className="text-xl text-gray-600 mb-2">No videos processed yet</h3>
        <p className="text-gray-400">Enter a URL above to extract recipes from a video</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {videos.map((video) => (
        <Card
          key={video.id}
          className="cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => onVideoClick(video)}
        >
          <CardContent className="p-0">
            <div className="relative aspect-video bg-gray-100 rounded-t-lg overflow-hidden">
              <img
                src={video.thumbnail}
                alt={video.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                <PlayCircle className="size-12 text-white" />
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-medium text-sm line-clamp-2 mb-2">{video.title}</h3>
              <p className="text-xs text-gray-500">
                {video.recipes.length} {video.recipes.length === 1 ? 'recipe' : 'recipes'} found
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {video.processedAt.toLocaleDateString()}
              </p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}