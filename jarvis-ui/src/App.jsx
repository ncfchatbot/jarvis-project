import { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState("");
  const [responseText, setResponseText] = useState("ระบบพร้อมทำงานครับเจ้านาย");
  const [isSoundOn, setIsSoundOn] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);

  // ฟังก์ชันบังคับพูดออกลำโพงแบบชัวร์ 100%
  const speakText = (textToSpeak) => {
    if (!isSoundOn) return;
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = 'th-TH';
    utterance.rate = 1.0;
    
    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;

    setIsLoading(true);
    setResponseText("กำลังประมวลผล...");

    try {
      const backendUrl = 'http://localhost:8001/chat';
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const reply = data.response || "รับทราบครับเจ้านาย";
      
      // อัปเดตข้อความบนจอ
      setResponseText(reply);
      
      // [จุดสำคัญ] สั่งให้ลำโพงพูดข้อความที่ได้จาก Python ออกมาทันทีตรงนี้!
      speakText(reply);

    } catch (error) {
      console.error("Jarvis System Error:", error);
      const errorMsg = "ขออภัยครับเจ้านาย ระบบขัดข้องครับ";
      setResponseText(errorMsg);
      speakText(errorMsg);
    } finally {
      setIsLoading(false);
      setInputText("");
    }
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("เบราว์เซอร์ไม่รองรับระบบสั่งงานด้วยเสียงครับ");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'th-TH';
    recognition.onresult = (event) => setInputText(event.results[0][0].transcript);
    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  return (
    <div className="min-h-screen bg-[#0a0f1a] text-cyan-400 flex flex-col items-center justify-center p-4 font-sans">
      <button 
        onClick={() => setIsSoundOn(!isSoundOn)}
        className="mb-10 px-6 py-2 border border-cyan-800 rounded-full text-cyan-400 hover:bg-cyan-900 transition flex items-center gap-2 tracking-widest text-sm shadow-[0_0_10px_rgba(34,211,238,0.2)]"
      >
        SOUND: {isSoundOn ? "ON" : "OFF"}
      </button>

      <div className="relative w-48 h-48 flex items-center justify-center mb-8">
        <div className={`absolute w-full h-full border-t-2 border-cyan-500 rounded-full ${isLoading ? 'animate-spin' : 'animate-[spin_3s_linear_infinite]'}`}></div>
        <div className={`absolute w-3/4 h-3/4 border-b-2 border-purple-500 rounded-full ${isLoading ? 'animate-spin' : 'animate-[spin_4s_linear_infinite_reverse]'}`}></div>
        <div className={`w-16 h-16 bg-cyan-400 rounded-full shadow-[0_0_30px_10px_rgba(34,211,238,0.5)] ${isLoading ? 'animate-ping' : 'animate-pulse'}`}></div>
      </div>

      <h2 className="tracking-widest text-sm mb-6 text-gray-500">SYSTEM ONLINE</h2>

      <div className="w-full max-w-md min-h-[80px] bg-[#111827] border border-gray-800 rounded-xl p-5 mb-8 text-center text-gray-300 shadow-lg flex items-center justify-center">
        {responseText}
      </div>

      <div className="w-full max-w-md flex gap-2">
        <button 
          onClick={startListening}
          className={`flex items-center justify-center p-3 rounded-xl border transition ${isListening ? 'bg-red-500 border-red-500 text-white animate-pulse' : 'bg-[#111827] border-cyan-900 text-cyan-400 hover:border-cyan-500'}`}
        >
          🎤
        </button>

        <div className="flex-1 bg-[#111827] border border-cyan-900 rounded-xl px-4 py-3 flex items-center focus-within:border-cyan-500 transition">
          <input 
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="พิมพ์คำถามที่นี่..."
            className="bg-transparent w-full outline-none text-white placeholder-gray-600"
          />
        </div>
        
        <button 
          onClick={handleSend}
          disabled={isLoading}
          className="bg-cyan-500 hover:bg-cyan-400 text-black font-bold px-6 py-3 rounded-xl transition disabled:opacity-50 tracking-wider"
        >
          SEND
        </button>
      </div>
    </div>
  );
}

export default App;