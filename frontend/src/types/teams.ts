export interface TeamMember {
  id: string;
  userId: string;
  name: string;
  email: string;
  role?: string;
}

export interface Team {
  id: string;
  eventId: string;
  name: string;
  inviteCode?: string;
  members: TeamMember[];
  createdAt: string;
}