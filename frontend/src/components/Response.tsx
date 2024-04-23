import React from "react";

interface ResponseProps {
  text: string;
}

const Response: React.FC<ResponseProps> = ({ text }) => {
  return (
    <div className="mt-4 prose">
      <h2 className="prose-xl">Response Text:</h2>
      <p className="prose">{text}</p>
    </div>
  );
};

export default Response;
