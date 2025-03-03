"use client";

import { useEffect, useState } from "react";
import InputBox from "./InputBox";

const defaultNum = 3;
export default function Home() {
  const [texts, setTexts] = useState(new Array(defaultNum).fill(""));
  const [rules, setRules] = useState(new Array(defaultNum).fill(""));
  const [output, setOutput] = useState("");

  useEffect(() => {
    setOutput(texts.join(""));
  }, [texts]);
  const setText = (i: number, text: string) =>
    setTexts([...texts.slice(0, i), text, ...texts.slice(i + 1)]);

  const setRule = (i: number, rule: string) =>
    setRules([...rules.slice(0, i), rule, ...rules.slice(i + 1)]);

  return (
    <ul className="function-list p-2 gap-1 flex-grow">
      {texts.map((text, i) => (
        <InputBox
          key={i}
          text={text}
          setText={(text) => setText(i, text)}
          rule={rules[i]}
          setRule={(rule) => setRule(i, rule)}
        />
      ))}
      <li>
        <p>{output}</p>
      </li>
    </ul>
  );
}
