import { Info, ClipboardCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "wouter";
import neuravoxLogo from "@assets/logo.png";

export function Header() {
  return (
    <header className="border-b">
      <div className="container max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2 hover:opacity-90 transition-opacity">
          <img src={neuravoxLogo} alt="Yesveri Logo" className="h-9 w-9" />
          <div className="flex flex-col">
            <span className="text-xl font-bold leading-tight">Yesveri</span>
            <span className="text-[10px] uppercase tracking-wider text-muted-foreground">Election Verification</span>
          </div>
        </Link>

        <nav className="flex items-center space-x-1">
          <Button variant="ghost" asChild size="sm">
            <Link href="/about">
              <Info className="h-4 w-4 mr-1.5" />
              About
            </Link>
          </Button>
          <Button asChild size="sm">
            <Link href="/verify">
              <ClipboardCheck className="h-4 w-4 mr-1.5" />
              Verify a Claim
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  );
}
