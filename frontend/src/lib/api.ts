const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token
          ? { Authorization: `Bearer ${token}` }
          : {}),
        ...(options.headers || {}),
      },
    }
  );

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const eventApi = {
  getAll: () =>
    request("/events"),

  getById: (eventId: string) =>
    request(`/events/${eventId}`),

  create: (data: unknown) =>
    request("/events", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  update: (eventId: string, data: unknown) =>
    request(`/events/${eventId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
};

export const teamApi = {
  getMyTeams: () =>
    request("/teams"),

  getById: (teamId: string) =>
    request(`/teams/${teamId}`),

  create: (data: unknown) =>
    request("/teams", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  join: (inviteCode: string) =>
    request("/teams/join", {
      method: "POST",
      body: JSON.stringify({ inviteCode }),
    }),

  invite: (teamId: string, email: string) =>
    request(`/teams/${teamId}/invite`, {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
};

export const submissionApi = {
  getAll: () =>
    request("/submissions"),

  getById: (submissionId: string) =>
    request(`/submissions/${submissionId}`),

  create: (data: unknown) =>
    request("/submissions", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  update: (submissionId: string, data: unknown) =>
    request(`/submissions/${submissionId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  submit: (submissionId: string) =>
    request(`/submissions/${submissionId}/submit`, {
      method: "POST",
    }),
};

export const judgingApi = {
  getAssignments: () =>
    request("/judges/assignments"),

  getRubric: (eventId: string) =>
    request(`/rubrics/${eventId}`),

  submitScore: (data: unknown) =>
    request("/scores", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getMyScores: () =>
    request("/scores/me"),
};

export const votingApi = {
  vote: (submissionId: string) =>
    request("/votes", {
      method: "POST",
      body: JSON.stringify({ submissionId }),
    }),

  removeVote: (submissionId: string) =>
    request(`/votes/${submissionId}`, {
      method: "DELETE",
    }),

  getResults: (eventId: string) =>
    request(`/votes/results/${eventId}`),
};

export const resultsApi = {
  get: (eventId: string) =>
    request(`/results/${eventId}`),

  exportCsv: (eventId: string) =>
    request(`/results/${eventId}/export`),
};