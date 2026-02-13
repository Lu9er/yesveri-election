import { CheckCircle, XCircle, AlertTriangle, HelpCircle, RefreshCw } from "lucide-react";
import type { AlignmentStatus } from "@/lib/api-types";

const config: Record<AlignmentStatus, {
  label: string;
  description: string;
  icon: typeof CheckCircle;
  className: string;
}> = {
  MATCHES: {
    label: "Matches Official Data",
    description: "This claim aligns with official Electoral Commission records.",
    icon: CheckCircle,
    className: "bg-green-50 border-green-200 text-green-800",
  },
  CONFLICTS: {
    label: "Conflicts with Official Data",
    description: "This claim contradicts official Electoral Commission records.",
    icon: XCircle,
    className: "bg-red-50 border-red-200 text-red-800",
  },
  NO_OFFICIAL_DATA: {
    label: "No Official Data Available",
    description: "No Electoral Commission announcement found for this claim.",
    icon: AlertTriangle,
    className: "bg-yellow-50 border-yellow-200 text-yellow-800",
  },
  CANNOT_VERIFY: {
    label: "Cannot Verify",
    description: "Not enough information to extract a verifiable election claim.",
    icon: HelpCircle,
    className: "bg-gray-50 border-gray-200 text-gray-700",
  },
  DATA_UPDATED: {
    label: "Official Data Updated",
    description: "Official EC data has changed since this claim was last checked.",
    icon: RefreshCw,
    className: "bg-blue-50 border-blue-200 text-blue-800",
  },
};

interface AlignmentBadgeProps {
  status: AlignmentStatus;
  compact?: boolean;
}

export function AlignmentBadge({ status, compact = false }: AlignmentBadgeProps) {
  const { label, description, icon: Icon, className } = config[status];

  if (compact) {
    return (
      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium border ${className}`}>
        <Icon className="h-4 w-4" />
        {label}
      </span>
    );
  }

  return (
    <div className={`flex items-start gap-3 p-4 rounded-lg border ${className}`}>
      <Icon className="h-6 w-6 mt-0.5 flex-shrink-0" />
      <div>
        <h3 className="font-semibold text-lg">{label}</h3>
        <p className="text-sm opacity-80 mt-0.5">{description}</p>
      </div>
    </div>
  );
}
