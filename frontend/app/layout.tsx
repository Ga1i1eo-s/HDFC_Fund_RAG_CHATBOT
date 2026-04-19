import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";
import FloatingCTA from "./components/FloatingCTA/FloatingCTA";
import ChatbotWidget from "./components/Chatbot/ChatbotWidget";

export const metadata: Metadata = {
  title: "HDFC AMC Investment Portal",
  description: "Manage your mutual funds and stock portfolio with HDFC AMC.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div style={{ display: 'flex', minHeight: '100vh' }}>
          <Sidebar />
          <div style={{ flex: 1, marginLeft: '250px', display: 'flex', flexDirection: 'column' }}>
            <Header />
            <main style={{ flex: 1 }}>
              {children}
            </main>
            <Footer />
          </div>
        </div>
        <FloatingCTA />
        <ChatbotWidget />
      </body>
    </html>
  );
}
