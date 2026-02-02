import { ExternalLink, ChefHat, ShoppingCart, Flame, Beef, Wheat, Droplet } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/app/components/ui/dialog";
import { ScrollArea } from "@/app/components/ui/scroll-area";
import { Separator } from "@/app/components/ui/separator";
import { Badge } from "@/app/components/ui/badge";
import { Button } from "@/app/components/ui/button";
import type { ProcessedVideo } from "./RecipeGallery";

interface RecipeDetailDialogProps {
  video: ProcessedVideo | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function RecipeDetailDialog({ video, open, onOpenChange }: RecipeDetailDialogProps) {
  if (!video) return null;

  const formatValue = (value: number | null | undefined, unit?: string) => {
    if (value === null || value === undefined) return "—";
    const formatted = Number.isFinite(value) ? value.toLocaleString() : String(value);
    return unit ? `${formatted}${unit}` : formatted;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <ChefHat className="size-5" />
            {video.title}
          </DialogTitle>
          <DialogDescription>
            Found {video.recipes.length} {video.recipes.length === 1 ? 'recipe' : 'recipes'} in this video
          </DialogDescription>
        </DialogHeader>
        
        <ScrollArea className="max-h-[60vh] pr-4">
          <div className="space-y-6">
            {video.recipes.map((recipe, index) => (
              <div key={index} className="border rounded-lg p-5">
                <div className="flex items-start justify-between mb-3">
                  <h3 className="text-lg font-semibold">{recipe.name}</h3>
                  <Badge variant="outline">Recipe {index + 1}</Badge>
                </div>
                
                <p className="text-sm text-gray-600 mb-4">{recipe.description}</p>
                
                {/* Nutritional Information */}
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
                  <h4 className="font-medium mb-3 text-sm text-gray-700">Nutritional Information (per serving)</h4>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="flex items-center gap-2 mb-1">
                        <Flame className="size-4 text-orange-500" />
                        <span className="text-xs text-gray-500">Calories</span>
                      </div>
                      <p className="text-xl font-bold text-gray-900">
                        {formatValue(recipe.nutrition.calories)}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="flex items-center gap-2 mb-1">
                        <Beef className="size-4 text-red-500" />
                        <span className="text-xs text-gray-500">Protein</span>
                      </div>
                      <p className="text-xl font-bold text-gray-900">
                        {formatValue(recipe.nutrition.protein, "g")}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="flex items-center gap-2 mb-1">
                        <Wheat className="size-4 text-amber-500" />
                        <span className="text-xs text-gray-500">Carbs</span>
                      </div>
                      <p className="text-xl font-bold text-gray-900">
                        {formatValue(recipe.nutrition.carbs, "g")}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="flex items-center gap-2 mb-1">
                        <Droplet className="size-4 text-yellow-500" />
                        <span className="text-xs text-gray-500">Fat</span>
                      </div>
                      <p className="text-xl font-bold text-gray-900">
                        {formatValue(recipe.nutrition.fat, "g")}
                      </p>
                    </div>
                  </div>
                  {(recipe.nutrition.fiber !== null && recipe.nutrition.fiber !== undefined) ||
                  (recipe.nutrition.sugar !== null && recipe.nutrition.sugar !== undefined) ||
                  (recipe.nutrition.sodium !== null && recipe.nutrition.sodium !== undefined) ? (
                    <div className="mt-3 pt-3 border-t border-white/50 flex flex-wrap gap-4 text-sm">
                      {recipe.nutrition.fiber !== null && recipe.nutrition.fiber !== undefined && (
                        <span className="text-gray-600">
                          <strong>Fiber:</strong> {formatValue(recipe.nutrition.fiber, "g")}
                        </span>
                      )}
                      {recipe.nutrition.sugar !== null && recipe.nutrition.sugar !== undefined && (
                        <span className="text-gray-600">
                          <strong>Sugar:</strong> {formatValue(recipe.nutrition.sugar, "g")}
                        </span>
                      )}
                      {recipe.nutrition.sodium !== null && recipe.nutrition.sodium !== undefined && (
                        <span className="text-gray-600">
                          <strong>Sodium:</strong> {formatValue(recipe.nutrition.sodium, "mg")}
                        </span>
                      )}
                    </div>
                  ) : null}
                </div>
                
                <Separator className="my-4" />
                
                <div className="mb-4">
                  <h4 className="font-medium mb-3 flex items-center gap-2">
                    <span className="bg-primary/10 text-primary px-2 py-1 rounded text-sm">
                      Steps
                    </span>
                  </h4>
                  <ol className="space-y-2">
                    {recipe.steps.map((step, stepIndex) => (
                      <li key={stepIndex} className="flex gap-3">
                        <span className="flex-shrink-0 size-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-medium">
                          {stepIndex + 1}
                        </span>
                        <span className="text-sm text-gray-700 pt-0.5">{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
                
                {recipe.purchaseLinks.length > 0 && (
                  <>
                    <Separator className="my-4" />
                    <div>
                      <h4 className="font-medium mb-3 flex items-center gap-2">
                        <ShoppingCart className="size-4" />
                        Where to Buy
                      </h4>
                      <div className="space-y-2">
                        {recipe.purchaseLinks.map((link, linkIndex) => (
                          <Button
                            key={linkIndex}
                            variant="outline"
                            size="sm"
                            className="w-full justify-between"
                            asChild
                          >
                            <a href={link.url} target="_blank" rel="noopener noreferrer">
                              <span className="text-sm">{link.item}</span>
                              <ExternalLink className="size-4" />
                            </a>
                          </Button>
                        ))}
                      </div>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}