import "./globals.css";
import Header from "../components/Header";

export const metadata = {
  title: "Marketing AI Assistant",
  description: "Fast, minimal, streaming QA interface"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <div className="container">{children}</div>
      </body>
    </html>
  );
}
