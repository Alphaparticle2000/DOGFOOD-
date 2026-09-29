export interface SubmissionResult {
  submissionId: string;
  projectTitle: string;
  rawScore: number;
  normalizedScore?: number;
  rank?: number;
}

export interface Result {
  eventId: string;
  results: SubmissionResult[];
}