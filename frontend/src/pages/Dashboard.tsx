import {
  ArrowRight,
  ArrowUpRight,
  CheckCircle2,
  Clock3,
  GitBranch,
  LayoutGrid,
  UsersRound,
} from "lucide-react";

import { Link } from "react-router-dom";
import fixtureData from "../data/fixtures.json";
import { useAuth } from "../hooks/useAuth";

type Project = {
  id: string;
  team: string;
  track: string;
  title: string;
  summary: string;
  repo_url: string;
  submitted_at: string;
};

const data = fixtureData as {
  event: {
    name: string;
    submissions_close: string;
  };

  tracks: {
    id: string;
    name: string;
  }[];

  teams: {
    id: string;
    name: string;
  }[];

  projects: Project[];

  judges: unknown[];

  scores: unknown[];
};

const trackName = (id: string) =>
  data.tracks.find(
    (track) => track.id === id
  )?.name ?? id;

export default function Dashboard() {
  const { user } = useAuth();

  const latest = [...data.projects]
    .sort(
      (a, b) =>
        b.submitted_at.localeCompare(
          a.submitted_at
        )
    )
    .slice(0, 3);

  return (
    <div>
      <header className="page-header">
        <div>
          <span className="eyebrow">
            WORKSPACE / OVERVIEW
          </span>

          <h1>
            Good evening,{" "}
            {user?.name ?? "Himanshu"}.
          </h1>

          <p>
            The competition at a glance —
            teams, projects, judging and the
            next deadline.
          </p>
        </div>

        <div
          className="header-actions"
          style={{
            display: "flex",
            gap: 8,
          }}
        >
          <Link
            to="/gallery"
            className="ghost-btn"
          >
            <LayoutGrid size={15} />
            Browse gallery
          </Link>

          <Link
            to="/submissions"
            className="primary-btn"
          >
            Open submission
            <ArrowUpRight size={15} />
          </Link>
        </div>
      </header>

      <section
        className="dashboard-grid"
        aria-label="Competition statistics"
      >
        <div className="stat-card featured">
          <span className="stat-label">
            PROJECTS
          </span>

          <strong className="stat-value">
            {data.projects.length}
          </strong>

          <div className="stat-foot">
            <GitBranch size={13} />
            live submissions
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-label">
            TEAMS
          </span>

          <strong className="stat-value">
            {data.teams.length}
          </strong>

          <div className="stat-foot">
            <UsersRound size={13} />
            registered teams
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-label">
            JUDGES
          </span>

          <strong className="stat-value">
            {data.judges.length}
          </strong>

          <div className="stat-foot">
            <CheckCircle2 size={13} />
            assigned reviewers
          </div>
        </div>

        <div className="stat-card">
          <span className="stat-label">
            SCORE RECORDS
          </span>

          <strong className="stat-value">
            {data.scores.length}
          </strong>

          <div className="stat-foot">
            <span className="stat-positive">
              ●
            </span>
            judging activity
          </div>
        </div>
      </section>

      <section className="notice-strip">
        <div className="notice-main">
          <div className="notice-icon">
            <Clock3 size={17} />
          </div>

          <div className="notice-copy">
            <strong>
              Submission window
            </strong>

            <span>
              Final project submissions close on{" "}
              {new Date(
                data.event.submissions_close
              ).toLocaleDateString(
                "en-IN",
                {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                }
              )}
              .
            </span>
          </div>
        </div>

        <div className="notice-time">
          <strong>OPEN</strong>
          <span>{data.event.name}</span>
        </div>

        <Link
          to="/submissions"
          className="text-btn"
        >
          Review status
          <ArrowRight size={13} />
        </Link>
      </section>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">
                LATEST
              </span>

              <h2>Project activity</h2>
            </div>

            <Link
              to="/gallery"
              className="text-btn"
            >
              View all
              <ArrowRight size={13} />
            </Link>
          </div>

          {latest.map((project, index) => (
            <article
              className="project-row"
              key={project.id}
            >
              <span className="project-no">
                0{index + 1}
              </span>

              <div className="project-info">
                <div className="project-title-line">
                  <h3>{project.title}</h3>

                  <span className="badge ok">
                    SUBMITTED
                  </span>
                </div>

                <div className="project-meta">
                  <span>
                    {trackName(project.track)}
                  </span>

                  <span className="bullet">
                    ·
                  </span>

                  <span>{project.team}</span>
                </div>
              </div>

              <div className="score-inline">
                <small>PROJECT</small>

                <strong>
                  {project.id.replace(
                    "prj_",
                    "#"
                  )}
                </strong>
              </div>

              <Link
                className="row-icon"
                to="/gallery"
                aria-label={`Open ${project.title}`}
              >
                <ArrowUpRight size={14} />
              </Link>
            </article>
          ))}

          <Link
            to="/gallery"
            className="panel-footer"
          >
            Explore all submissions
          </Link>
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <span className="eyebrow">
                SYSTEM
              </span>

              <h2>What’s moving</h2>
            </div>
          </div>

          <div className="activity-list">
            <div className="activity-item">
              <div className="activity-icon">
                <GitBranch size={15} />
              </div>

              <div className="activity-copy">
                <strong>
                  Submission pipeline active
                </strong>

                <p>
                  {data.projects.length} projects
                  are currently visible in the
                  fixture dataset.
                </p>
              </div>

              <span className="activity-time">
                NOW
              </span>
            </div>

            <div className="activity-item">
              <div className="activity-icon">
                <UsersRound size={15} />
              </div>

              <div className="activity-copy">
                <strong>
                  Team formation is open
                </strong>

                <p>
                  {data.teams.length} teams are
                  represented in the current event
                  snapshot.
                </p>
              </div>

              <span className="activity-time">
                LIVE
              </span>
            </div>

            <div className="activity-item">
              <div className="activity-icon">
                <CheckCircle2 size={15} />
              </div>

              <div className="activity-copy">
                <strong>
                  Judging data is present
                </strong>

                <p>
                  {data.scores.length} score records
                  are available to the backend.
                </p>
              </div>

              <span className="activity-time">
                SYNCED
              </span>
            </div>
          </div>
        </section>
      </div>

      <section className="quick-grid">
        <Link
          to="/teams"
          className="quick-card"
        >
          <div>
            <span>TEAM SPACE</span>
            <strong>Manage your team</strong>
          </div>

          <UsersRound size={18} />
        </Link>

        <Link
          to="/judging"
          className="quick-card"
        >
          <div>
            <span>REVIEW</span>
            <strong>Open judging queue</strong>
          </div>

          <CheckCircle2 size={18} />
        </Link>

        <Link
          to="/results"
          className="quick-card"
        >
          <div>
            <span>OUTCOME</span>
            <strong>View results</strong>
          </div>

          <ArrowUpRight size={18} />
        </Link>
      </section>
    </div>
  );
}