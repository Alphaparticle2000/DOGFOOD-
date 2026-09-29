export interface Submission {
  id: string;
  teamId: string;
  projectId?: string;
  title: string;
  summary: string;
  description?: string;
  trackId: string;
  repoUrl?: string;
  demoUrl?: string;
  submissionUrl?: string;
  submittedAt?: string;
  updatedAt?: string;
  status: "draft" | "submitted" | "closed";
}