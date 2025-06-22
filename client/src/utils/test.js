// test.js
import { io } from "socket.io-client";

const socket = io("http://localhost:8000"); 

socket.on("connect", () => {
  console.log("✔ connected", socket.id);
  socket.emit("analyze_company", { company_name: "Meta" });
});

socket.on("status",  d => console.log("status:", d));
socket.on("analysis_complete", d => { console.log("done:", d); socket.disconnect(); });
socket.on("error",   e => { console.error("err:", e); socket.disconnect(); });
