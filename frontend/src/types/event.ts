export interface Event {
  id: string;
  name: string;
  description?: string;
  startDate: string;
  endDate: string;
  submissionDeadline: string;
  status: "upcoming" | "active" | "closed";
}

export interface Track {
  id: string;
  eventId: string;
  name: string;
  description?: string;
}

export interface Prize {
  id: string;
  eventId: string;
  name: string;
  amount?: number;
  description?: string;
}