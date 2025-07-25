
const BASE_URL = import.meta.env.VITE_BACKEND_URL;

export async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export async function embedDocument(filename: string) {
  const res = await fetch(`${BASE_URL}/embed?filename=${filename}`, {
    method: "POST",
  });
  return res.json();
}

export async function getReasoning(query: string, filename: string) {
  const params = new URLSearchParams({ query, filename });
  const res = await fetch(`${BASE_URL}/reason?${params.toString()}`, {
    method: "POST",
  });
  return res.json();
}
