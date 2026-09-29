import { useEffect } from "react";

import { eventApi } from "../lib/api";
import { useApi } from "../hooks/useApi";

export default function Events() {
  const {
    data,
    loading,
    error,
    execute,
  } = useApi(eventApi.getAll);

  useEffect(() => {
    execute();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      {/* UI later */}

      <pre>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}