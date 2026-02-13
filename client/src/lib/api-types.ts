export type AlignmentStatus =
  | "MATCHES"
  | "CONFLICTS"
  | "NO_OFFICIAL_DATA"
  | "CANNOT_VERIFY"
  | "DATA_UPDATED";

export interface ExtractedFields {
  candidate_name: string | null;
  party: string | null;
  position: string | null;
  district: string | null;
  vote_count: number | null;
  percentage: number | null;
  result_claim: string | null;
}

export interface OfficialData {
  candidate_name: string;
  party: string;
  position: string;
  district: string;
  vote_count: number;
  percentage: number;
  total_votes: number;
  source_name: string;
  source_url: string | null;
  last_updated: string;
}

export interface SourceReference {
  name: string;
  url: string | null;
  last_updated: string;
}

export interface VerificationResponse {
  alignment: AlignmentStatus;
  extracted_fields: ExtractedFields;
  official_data: OfficialData | null;
  explanation: string;
  confidence: number;
  source_reference: SourceReference | null;
  verified_at: string;
}

export interface ImageVerificationResponse extends VerificationResponse {
  extracted_text: string;
}

export interface SourceInfo {
  id: number;
  name: string;
  url: string | null;
  district: string;
  position: string;
  last_scraped: string | null;
  result_count: number;
}

export interface HealthResponse {
  status: string;
  database: boolean;
  redis: boolean;
  ec_data_last_updated: string | null;
  total_official_results: number;
}
