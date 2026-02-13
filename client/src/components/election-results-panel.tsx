import { AlignmentBadge } from "@/components/ui/alignment-badge";
import { FieldComparison } from "@/components/field-comparison";
import { SourceReference } from "@/components/source-reference";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { Lock } from "lucide-react";
import type { VerificationResponse, ImageVerificationResponse } from "@/lib/api-types";

interface ElectionResultsPanelProps {
  result: VerificationResponse | ImageVerificationResponse;
}

export function ElectionResultsPanel({ result }: ElectionResultsPanelProps) {
  const isImageResult = "extracted_text" in result;
  const confidencePct = Math.round(result.confidence * 100);

  return (
    <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Alignment Status Banner */}
      <div className="p-6">
        <AlignmentBadge status={result.alignment} />
      </div>

      <Separator />

      {/* Explanation */}
      <div className="p-6">
        <h4 className="text-sm font-medium text-muted-foreground mb-2">
          Explanation
        </h4>
        <p className="text-gray-800 leading-relaxed">{result.explanation}</p>
      </div>

      <Separator />

      {/* OCR Extracted Text (image claims only) */}
      {isImageResult && (result as ImageVerificationResponse).extracted_text && (
        <>
          <div className="p-6">
            <h4 className="text-sm font-medium text-muted-foreground mb-2">
              Text Extracted from Image
            </h4>
            <div className="bg-gray-50 rounded-md p-3 text-sm text-gray-700 font-mono whitespace-pre-wrap">
              {(result as ImageVerificationResponse).extracted_text}
            </div>
          </div>
          <Separator />
        </>
      )}

      {/* Field Comparison */}
      <div className="p-6">
        <h4 className="text-sm font-medium text-muted-foreground mb-3">
          Claim vs Official Record
        </h4>
        <FieldComparison
          extracted={result.extracted_fields}
          official={result.official_data}
        />
      </div>

      <Separator />

      {/* Verification Confidence */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-muted-foreground">
            Verification Confidence
          </h4>
          <span className="text-sm font-medium">{confidencePct}%</span>
        </div>
        <Progress value={confidencePct} className="h-2" />
        <p className="text-xs text-muted-foreground mt-1.5">
          Based on how many extracted fields could be matched against official
          records
        </p>
      </div>

      {/* Source Reference */}
      {result.source_reference && (
        <>
          <Separator />
          <div className="p-6">
            <SourceReference source={result.source_reference} />
          </div>
        </>
      )}

      <Separator />

      {/* Privacy Notice */}
      <div className="p-4 bg-gray-50 flex items-center gap-2 text-xs text-muted-foreground">
        <Lock className="h-3.5 w-3.5 flex-shrink-0" />
        <span>
          We do not store uploaded images or claim text. Only anonymized metrics
          are logged. All data auto-deletes after 24 hours.
        </span>
      </div>
    </div>
  );
}
