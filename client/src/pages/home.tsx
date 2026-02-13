import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { ClaimForm } from "@/components/claim-form";
import { ElectionResultsPanel } from "@/components/election-results-panel";
import { LoadingState } from "@/components/loading-state";
import { EmptyState } from "@/components/empty-state";
import { useToast } from "@/hooks/use-toast";
import type { VerificationResponse, ImageVerificationResponse } from "@/lib/api-types";



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
    <div className="container max-w-4xl mx-auto px-4 py-8">
      <ClaimForm
        onSubmitText={handleSubmitText}
        onSubmitImage={handleSubmitImage}
        isVerifying={isVerifying}
      />

      {isVerifying && <LoadingState />}

      {!isVerifying && !result && <EmptyState />}

      {!isVerifying && result && <ElectionResultsPanel result={result} />}
    </div>
  );
}
