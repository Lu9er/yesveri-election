import { ClipboardCheck } from "lucide-react";

export function EmptyState() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
      <div className="flex flex-col items-center justify-center py-6">
        <ClipboardCheck className="h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-1">No claim verified yet</h3>
        <p className="text-sm text-gray-500 mb-4">
          Enter an election claim above or upload a screenshot to check it against official EC data
        </p>
      </div>
    </div>
  );
}
