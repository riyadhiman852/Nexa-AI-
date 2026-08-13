"use client";

import { useEffect, useState } from "react";

type Stats = {
  total: number;
  successful: number;
  failed: number;
};

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    total: 0,
    successful: 0,
    failed: 0,
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchStats = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analytics",
        {
          cache: "no-store",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch analytics");
      }

      const data = await response.json();

      setStats(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError(
        "Analytics server is not running. Start the backend analytics API."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();

    const interval = setInterval(fetchStats, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <main
      style={{
        minHeight: "100vh",
        padding: "40px",
        background: "#f8fafc",
        color: "#0f172a",
      }}
    >
      <div
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
        }}
      >
        <div style={{ marginBottom: "35px" }}>
          <h1
            style={{
              fontSize: "36px",
              fontWeight: 700,
              marginBottom: "8px",
            }}
          >
            Nexa AI
          </h1>

          <p
            style={{
              fontSize: "18px",
              color: "#64748b",
            }}
          >
            Call Analytics Dashboard
          </p>
        </div>

        {error && (
          <div
            style={{
              padding: "15px",
              marginBottom: "25px",
              borderRadius: "10px",
              background: "#fee2e2",
              color: "#991b1b",
            }}
          >
            {error}
          </div>
        )}

        {loading ? (
          <p>Loading analytics...</p>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(220px, 1fr))",
              gap: "20px",
            }}
          >
            <div
              style={{
                background: "white",
                padding: "30px",
                borderRadius: "16px",
                boxShadow:
                  "0 4px 15px rgba(0, 0, 0, 0.08)",
              }}
            >
              <p
                style={{
                  color: "#64748b",
                  marginBottom: "10px",
                }}
              >
                Total Calls
              </p>

              <h2
                style={{
                  fontSize: "42px",
                  margin: 0,
                }}
              >
                {stats.total}
              </h2>
            </div>

            <div
              style={{
                background: "white",
                padding: "30px",
                borderRadius: "16px",
                boxShadow:
                  "0 4px 15px rgba(0, 0, 0, 0.08)",
              }}
            >
              <p
                style={{
                  color: "#64748b",
                  marginBottom: "10px",
                }}
              >
                Successful Calls
              </p>

              <h2
                style={{
                  fontSize: "42px",
                  margin: 0,
                }}
              >
                {stats.successful}
              </h2>
            </div>

            <div
              style={{
                background: "white",
                padding: "30px",
                borderRadius: "16px",
                boxShadow:
                  "0 4px 15px rgba(0, 0, 0, 0.08)",
              }}
            >
              <p
                style={{
                  color: "#64748b",
                  marginBottom: "10px",
                }}
              >
                Failed Calls
              </p>

              <h2
                style={{
                  fontSize: "42px",
                  margin: 0,
                }}
              >
                {stats.failed}
              </h2>
            </div>
          </div>
        )}

        <div
          style={{
            marginTop: "35px",
            padding: "20px",
            background: "white",
            borderRadius: "12px",
            color: "#64748b",
          }}
        >
          <p style={{ margin: 0 }}>
            Dashboard updates automatically every 3 seconds.
          </p>
        </div>
      </div>
    </main>
  );
}