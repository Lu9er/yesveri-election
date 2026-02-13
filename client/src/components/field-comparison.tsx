import { CheckCircle, XCircle, Minus } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { ExtractedFields, OfficialData } from "@/lib/api-types";

interface FieldComparisonProps {
  extracted: ExtractedFields;
  official: OfficialData | null;
}

function formatNumber(n: number | null | undefined): string {
  if (n == null) return "Not detected";
  return n.toLocaleString();
}

function formatPercentage(n: number | null | undefined): string {
  if (n == null) return "Not detected";
  return `${n}%`;
}

function formatValue(v: string | number | null | undefined): string {
  if (v == null) return "Not detected";
  return String(v);
}

interface FieldRow {
  label: string;
  claimed: string;
  official: string;
  match: "match" | "mismatch" | "na";
}

export function FieldComparison({ extracted, official }: FieldComparisonProps) {
  const rows: FieldRow[] = [];

  const addRow = (
    label: string,
    claimedVal: string | number | null | undefined,
    officialVal: string | number | null | undefined,
    formatter: (v: string | number | null | undefined) => string = formatValue,
    compareFn?: (a: any, b: any) => boolean,
  ) => {
    const claimed = formatter(claimedVal);
    const officialStr = official ? formatter(officialVal) : "N/A";

    let match: "match" | "mismatch" | "na" = "na";
    if (claimedVal != null && official && officialVal != null) {
      if (compareFn) {
        match = compareFn(claimedVal, officialVal) ? "match" : "mismatch";
      } else {
        match =
          String(claimedVal).toLowerCase() === String(officialVal).toLowerCase()
            ? "match"
            : "mismatch";
      }
    }

    rows.push({ label, claimed, official: officialStr, match });
  };

  addRow("Candidate", extracted.candidate_name, official?.candidate_name, formatValue, (a, b) =>
    b.toLowerCase().includes(a.toLowerCase()),
  );
  addRow("Party", extracted.party, official?.party);
  addRow("District", extracted.district, official?.district, formatValue, (a, b) =>
    b.toLowerCase().includes(a.toLowerCase()),
  );
  addRow("Vote Count", extracted.vote_count, official?.vote_count, formatNumber, (a, b) =>
    Math.abs(a - b) / Math.max(a, b) < 0.01,
  );
  addRow("Percentage", extracted.percentage, official?.percentage, formatPercentage, (a, b) =>
    Math.abs(a - b) <= 0.5,
  );

  if (extracted.position || official?.position) {
    addRow("Position", extracted.position, official?.position);
  }

  return (
    <div className="rounded-lg border overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[140px]">Field</TableHead>
            <TableHead>Your Claim</TableHead>
            <TableHead>Official EC Data</TableHead>
            <TableHead className="w-[60px] text-center">Match</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.label}>
              <TableCell className="font-medium text-muted-foreground">
                {row.label}
              </TableCell>
              <TableCell>{row.claimed}</TableCell>
              <TableCell>{row.official}</TableCell>
              <TableCell className="text-center">
                {row.match === "match" && (
                  <CheckCircle className="h-5 w-5 text-green-600 mx-auto" />
                )}
                {row.match === "mismatch" && (
                  <XCircle className="h-5 w-5 text-red-600 mx-auto" />
                )}
                {row.match === "na" && (
                  <Minus className="h-5 w-5 text-gray-400 mx-auto" />
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
