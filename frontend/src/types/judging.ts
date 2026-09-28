export interface Judge {
    id: string;
    userId: string;
    assignedTracks: string[];
}

export interface Score {
    judgeId: string;
    projectId: string;
    functionality: number;
    quality: number;
    comment: string;
}