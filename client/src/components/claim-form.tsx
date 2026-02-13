import { useState, useRef, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { FileText, ImageIcon, Upload, X } from "lucide-react";

interface ClaimFormProps {
  onSubmitText: (data: { claim_text: string }) => void;
  onSubmitImage: (data: { image: File }) => void;
  isVerifying: boolean;
}

const MAX_CHARS = 1000;
const MAX_IMAGE_MB = 5;

export function ClaimForm({ onSubmitText, onSubmitImage, isVerifying }: ClaimFormProps) {
  const [activeTab, setActiveTab] = useState<string>("text");
  const [claimText, setClaimText] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setClaimText(e.target.value);
  };

  const processImageFile = useCallback(
    (file: File) => {
      if (file.size > MAX_IMAGE_MB * 1024 * 1024) {
        toast({
          title: "File too large",
          description: `Please select an image under ${MAX_IMAGE_MB}MB.`,
          variant: "destructive",
        });
        return;
      }

      const validTypes = ["image/jpeg", "image/png", "image/webp"];
      if (!validTypes.includes(file.type)) {
        toast({
          title: "Invalid file type",
          description: "Please upload a JPG, PNG, or WebP image.",
          variant: "destructive",
        });
        return;
      }

      setImageFile(file);
      const reader = new FileReader();
      reader.onload = (e) => setImagePreview(e.target?.result as string);
      reader.readAsDataURL(file);
    },
    [toast],
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) processImageFile(file);
  };

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) processImageFile(file);
    },
    [processImageFile],
  );

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => setIsDragOver(false);

  const clearImage = () => {
    setImageFile(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSubmit = () => {
    if (activeTab === "text") {
      if (!claimText.trim()) {
        toast({
          title: "Empty claim",
          description: "Please enter an election claim to verify.",
          variant: "destructive",
        });
        return;
      }
      if (claimText.length > MAX_CHARS) {
        toast({
          title: "Claim too long",
          description: `Please limit your claim to ${MAX_CHARS} characters.`,
          variant: "destructive",
        });
        return;
      }
      onSubmitText({ claim_text: claimText });
    } else {
      if (!imageFile) {
        toast({
          title: "No image selected",
          description: "Please upload a screenshot or photo to verify.",
          variant: "destructive",
        });
        return;
      }
      onSubmitImage({ image: imageFile });
    }
  };

  return (
    <div className="mb-8 bg-white rounded-lg shadow-sm p-6 border border-gray-200">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-medium text-gray-800">
            Verify Election Claim
          </h2>
        </div>

        <Tabs
          defaultValue="text"
          value={activeTab}
          onValueChange={setActiveTab}
          className="w-full mb-6"
        >
          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="text" disabled={isVerifying}>
              <FileText className="w-4 h-4 mr-2" />
              Text Claim
            </TabsTrigger>
            <TabsTrigger value="image" disabled={isVerifying}>
              <ImageIcon className="w-4 h-4 mr-2" />
              Image / Screenshot
            </TabsTrigger>
          </TabsList>

          <TabsContent value="text" className="mt-0">
            <Textarea
              id="claim"
              placeholder="e.g., 'Museveni won Kampala district with 65% of the vote' or 'Bobi Wine got 3.8 million votes nationally'"
              value={claimText}
              onChange={handleTextChange}
              className="resize-none min-h-[120px]"
              disabled={isVerifying}
            />
            <div className="flex justify-between items-center mt-2">
              <p className="text-xs text-gray-500">
                Paste any election claim — from WhatsApp, social media, or
                conversation
              </p>
              <div className="text-sm text-gray-500">
                <span>{claimText.length}</span> / {MAX_CHARS} characters
              </div>
            </div>
          </TabsContent>

          <TabsContent value="image" className="mt-0">
            {!imagePreview ? (
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                  isDragOver
                    ? "border-primary bg-primary/5"
                    : "border-gray-300 hover:border-primary/50"
                }`}
                onClick={() => fileInputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
              >
                <Upload className="h-8 w-8 mx-auto mb-3 text-gray-400" />
                <p className="text-sm text-gray-600 mb-1">
                  Drop a screenshot here, or click to browse
                </p>
                <p className="text-xs text-gray-400">
                  JPG, PNG, or WebP up to {MAX_IMAGE_MB}MB — WhatsApp
                  screenshots, social media posts, etc.
                </p>
              </div>
            ) : (
              <div className="relative border rounded-lg overflow-hidden">
                <img
                  src={imagePreview}
                  alt="Uploaded claim"
                  className="max-h-[200px] mx-auto object-contain"
                />
                <button
                  onClick={clearImage}
                  className="absolute top-2 right-2 bg-white/90 rounded-full p-1 hover:bg-white shadow-sm"
                  disabled={isVerifying}
                >
                  <X className="h-4 w-4" />
                </button>
                <div className="p-2 bg-gray-50 text-xs text-gray-500 text-center">
                  {imageFile?.name} ({(imageFile!.size / 1024).toFixed(0)} KB)
                </div>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={handleFileSelect}
              className="hidden"
            />
          </TabsContent>
        </Tabs>

        <div className="flex justify-end">
          <Button
            onClick={handleSubmit}
            disabled={
              isVerifying ||
              (activeTab === "text" ? !claimText.trim() : !imageFile)
            }
          >
            {activeTab === "text" ? "Check Claim" : "Upload & Check"}
          </Button>
        </div>
      </div>
    </div>
  );
}
