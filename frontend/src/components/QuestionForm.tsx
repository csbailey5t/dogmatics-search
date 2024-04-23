import { type FormEvent, useState } from "react";
import Response from "./Response";

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
    <div>
      <form onSubmit={submit} className="prose">
        <label className="form-label prose-xl">
          Question
          <textarea
            name="text"
            cols={65}
            className="block form-textarea rounded-md"
          />
        </label>
        <button
          type="submit"
          className="block border border-black my-2 p-2 rounded-md hover:bg-slate-100"
        >
          Submit
        </button>
      </form>
      {responseMessage && <Response text={responseMessage} />}
    </div>
  );
}
