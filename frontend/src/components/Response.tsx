import React from "react";

interface ResponseProps {
  text: string;
  responseSource: string;
}

const Response: React.FC<ResponseProps> = ({ text, responseSource }) => {
  return (
    <div className="mt-4 prose">
      <h2 className="prose-xl">Response Text:</h2>
      <p className="prose">{text}</p>
      <p className="prose">This response drew from: {responseSource}</p>
    </div>
  );
};

export default Response;
