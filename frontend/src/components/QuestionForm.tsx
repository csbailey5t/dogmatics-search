import { type FormEvent, useState } from "react";

export default function QuestionForm() {
  const [responseMessage, setResponseMessage] = useState("");

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const formDataObject = Object.fromEntries(formData.entries());
    const response = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formDataObject),
    });
    const data = await response.json();
    console.log(data);
    if (data.response) {
      setResponseMessage(data.response);
    }
  }
  return (
    <form onSubmit={submit}>
      <label>
        Question
        <input type="text" name="text" />
      </label>
      <button type="submit">Submit</button>
      {responseMessage && <p>{responseMessage}</p>}
    </form>
  );
}
