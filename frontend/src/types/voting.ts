export interface RubricCriterion {
  id: string;
  name: string;
  description?: string;
  weight: number;
  maxScore: number;
}

export interface Rubric {
  id: string;
  eventId: string;
  name: string;
  criteria: RubricCriterion[];
}

export interface JudgeAssignment {
  id: string;
  judgeId: string;
  submissionId: string;
  trackId: string;
}

export interface Score {
  id: string;
  judgeId: string;
  submissionId: string;
  criterionId: string;
  score: number;
  comment?: string;
}

export interface ScorePayload {
  submissionId: string;
  scores: {
    criterionId: string;
    score: number;
    comment?: string;
  }[];
}