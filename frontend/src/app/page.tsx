import { FeaturesBento } from "@/components/landing/features-bento";
import { FinalCta } from "@/components/landing/final-cta";
import { HeroSection } from "@/components/landing/hero-section";
import { HowItWorks } from "@/components/landing/how-it-works";
import { LandingFooter } from "@/components/landing/landing-footer";
import { LandingNav } from "@/components/landing/landing-nav";
import { MeshBackground } from "@/components/landing/mesh-background";
import { ProblemBento } from "@/components/landing/problem-bento";
import { SolutionPanel } from "@/components/landing/solution-panel";

export default function Home() {
  return (
    <div className="relative min-h-svh antialiased">
      <MeshBackground />
      <LandingNav />
      <main className="relative">
        <HeroSection />
        <ProblemBento />
        <SolutionPanel />
        <FeaturesBento />
        <HowItWorks />
        <FinalCta />
      </main>
      <LandingFooter />
    </div>
  );
}
