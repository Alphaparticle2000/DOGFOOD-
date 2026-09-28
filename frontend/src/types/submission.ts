type SubmissionStatus = "Draft" | "Submitted" | "Cancelled" 

export interface Submission{
    id: string;
    projectId: string;
    teamId: string;
    title: string;
    summary: string;
    repoUrl: string;
    status: SubmissionStatus;
    submittedAt: string;
}