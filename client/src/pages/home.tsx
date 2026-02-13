import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { ClaimForm } from "@/components/claim-form";
import { ElectionResultsPanel } from "@/components/election-results-panel";
import { LoadingState } from "@/components/loading-state";
import { EmptyState } from "@/components/empty-state";
import { useToast } from "@/hooks/use-toast";
import type { VerificationResponse, ImageVerificationResponse } from "@/lib/api-types";
import { Shield, Eye, Zap, Lock } from "lucide-react";

export default function Home() {
  const [result, setResult] = useState<VerificationResponse | ImageVerificationResponse | null>(null);
  const { toast } = useToast();

  const textMutation = useMutation({
    mutationFn: async (data: { claim_text: string }) => {
      const res = await apiRequest("POST", "/api/verify/text", data);
      return (await res.json()) as VerificationResponse;
    },
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      toast({
        title: "Verification failed",
        description: error.message || "Could not verify claim. Please try again.",
        variant: "destructive",
      });
    },
  });

  const apiBase = import.meta.env.VITE_API_URL ?? "";

  const imageMutation = useMutation({
    mutationFn: async (data: { image: File }) => {
      const formData = new FormData();
      formData.append("image", data.image);
      const res = await fetch(`${apiBase}/api/verify/image`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || "Image verification failed");
      }
      return (await res.json()) as ImageVerificationResponse;
    },
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      toast({
        title: "Verification failed",
        description: error.message || "Could not process image. Please try again.",
        variant: "destructive",
      });
    },
  });

  const isVerifying = textMutation.isPending || imageMutation.isPending;

  const handleSubmitText = (data: { claim_text: string }) => {
    toast({
      title: "Checking claim...",
      description: "Comparing against official Electoral Commission records.",
    });
    textMutation.mutate(data);
  };

  const handleSubmitImage = (data: { image: File }) => {
    toast({
      title: "Processing image...",
      description: "Extracting text and comparing against official records.",
    });
    imageMutation.mutate(data);
  };

  return (
    <div className="container max-w-6xl px-4">
      <main>
        <ClaimForm
          onSubmitText={handleSubmitText}
          onSubmitImage={handleSubmitImage}
          isVerifying={isVerifying}
        />

        {isVerifying && <LoadingState />}

        {!isVerifying && !result && <EmptyState />}

        {!isVerifying && result && <ElectionResultsPanel result={result} />}
      </main>

      {/* About Section */}
      <section className="mt-24 mb-16">
        <div className="bg-gradient-to-r from-primary/10 to-background p-8 rounded-lg shadow-sm">
          <h2 className="text-3xl font-bold mb-6">How Yesveri Works</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                <Shield className="h-5 w-5 text-primary" />
                Official Sources Only
              </h3>
              <p className="text-muted-foreground mb-4">
                We compare claims exclusively against official Uganda Electoral
                Commission announcements. Every data point is stored with its
                source URL and retrieval timestamp.
              </p>

              <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                <Eye className="h-5 w-5 text-primary" />
                Transparent Matching
              </h3>
              <p className="text-muted-foreground mb-4">
                We don't declare truth or falsehood. We show what we extracted
                from your claim, what the official record says, and let you
                judge the alignment.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Text and Image Support
              </h3>
              <p className="text-muted-foreground mb-4">
                Paste text claims directly, or upload WhatsApp screenshots and
                social media posts. Our OCR extracts the text, then checks it
                against EC data.
              </p>

              <h3 className="text-xl font-semibold mb-3 flex items-center gap-2">
                <Lock className="h-5 w-5 text-primary" />
                Privacy First
              </h3>
              <p className="text-muted-foreground">
                Uploaded images are never stored. Claim text is anonymized
                before logging and auto-deleted after 24 hours. We keep no
                personal information.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
