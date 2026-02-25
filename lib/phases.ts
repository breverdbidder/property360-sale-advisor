export interface ChecklistItem {
  id: string;
  text: string;
  critical: boolean;
}

export interface Phase {
  id: number;
  title: string;
  description: string;
  icon: string;
  items: ChecklistItem[];
}

export const PHASES: Phase[] = [
  {
    id: 1,
    title: "Financial Assessment",
    description: "Understand your current equity position and tax implications",
    icon: "💰",
    items: [
      { id: "1-1", text: "Calculate current mortgage payoff amount", critical: true },
      { id: "1-2", text: "Estimate net equity after commissions and closing costs", critical: true },
      { id: "1-3", text: "Review capital gains tax exposure (1031 exchange eligibility?)", critical: true },
      { id: "1-4", text: "Assess depreciation recapture liability", critical: false },
      { id: "1-5", text: "Review any prepayment penalties on existing loans", critical: false },
      { id: "1-6", text: "Calculate cash-on-cash return vs. reinvestment alternatives", critical: false },
    ],
  },
  {
    id: 2,
    title: "Property Condition Review",
    description: "Document property state to maximize value and avoid surprises",
    icon: "🔍",
    items: [
      { id: "2-1", text: "Commission pre-listing inspection report", critical: true },
      { id: "2-2", text: "Address deferred maintenance items (roof, HVAC, plumbing)", critical: true },
      { id: "2-3", text: "Photograph all units — interior and exterior", critical: false },
      { id: "2-4", text: "Document all recent capital improvements with receipts", critical: false },
      { id: "2-5", text: "Verify permits pulled and closed for all improvements", critical: true },
      { id: "2-6", text: "Check for environmental issues (mold, asbestos, lead paint)", critical: true },
    ],
  },
  {
    id: 3,
    title: "Tenancy & Lease Audit",
    description: "Clean up the rent roll before showing to buyers",
    icon: "📋",
    items: [
      { id: "3-1", text: "Compile all current leases with expiration dates", critical: true },
      { id: "3-2", text: "Document all current rents vs. market rents", critical: true },
      { id: "3-3", text: "Identify month-to-month vs. fixed-term tenants", critical: false },
      { id: "3-4", text: "Resolve any delinquent tenants before listing", critical: true },
      { id: "3-5", text: "Review security deposit compliance per FL Statute 83.49", critical: true },
      { id: "3-6", text: "Prepare 12-month rent roll in XLSX format", critical: false },
    ],
  },
  {
    id: 4,
    title: "Income Optimization",
    description: "Maximize NOI to improve cap rate and buyer appeal",
    icon: "📈",
    items: [
      { id: "4-1", text: "Raise below-market rents where lease permits", critical: true },
      { id: "4-2", text: "Bill-back utilities to tenants if not already doing so", critical: false },
      { id: "4-3", text: "Add or audit coin laundry, parking, storage income", critical: false },
      { id: "4-4", text: "Reduce vacancy by filling empty units before listing", critical: true },
      { id: "4-5", text: "Document all ancillary income streams", critical: false },
      { id: "4-6", text: "Calculate stabilized NOI for marketing package", critical: true },
    ],
  },
  {
    id: 5,
    title: "Legal & Title Prep",
    description: "Clear title issues and prepare legal docs for smooth closing",
    icon: "⚖️",
    items: [
      { id: "5-1", text: "Order preliminary title search", critical: true },
      { id: "5-2", text: "Resolve any liens, judgments, or encumbrances", critical: true },
      { id: "5-3", text: "Confirm entity ownership is current (LLC operating agreement)", critical: true },
      { id: "5-4", text: "Review any easements or deed restrictions affecting value", critical: false },
      { id: "5-5", text: "Confirm property taxes are current (no certificates outstanding)", critical: true },
      { id: "5-6", text: "Engage real estate attorney for contract review", critical: false },
    ],
  },
  {
    id: 6,
    title: "Valuation & Pricing",
    description: "Price correctly from day one to attract institutional buyers",
    icon: "🏷️",
    items: [
      { id: "6-1", text: "Order independent MAI appraisal or broker opinion of value", critical: true },
      { id: "6-2", text: "Pull 12-month comparable sales (cap rates, GRM)", critical: true },
      { id: "6-3", text: "Calculate value using income approach, sales comparison, cost", critical: false },
      { id: "6-4", text: "Set list price strategy: aggressive vs. value-add positioning", critical: true },
      { id: "6-5", text: "Model buyer underwriting at 3 cap rate scenarios", critical: false },
      { id: "6-6", text: "Define minimum acceptable net proceeds", critical: true },
    ],
  },
  {
    id: 7,
    title: "Marketing Package",
    description: "Build a compelling OM that sells before buyers visit",
    icon: "📦",
    items: [
      { id: "7-1", text: "Create Offering Memorandum (OM) with financials and photos", critical: true },
      { id: "7-2", text: "Professional photography and drone video", critical: false },
      { id: "7-3", text: "Build 3-year proforma with value-add projections", critical: true },
      { id: "7-4", text: "List on LoopNet, CoStar, Crexi, and MLS (if applicable)", critical: true },
      { id: "7-5", text: "Target direct outreach to 1031 exchange buyers", critical: false },
      { id: "7-6", text: "Set up data room (NDA-gated) for due diligence docs", critical: true },
    ],
  },
  {
    id: 8,
    title: "Offer & Negotiation",
    description: "Qualify buyers and negotiate terms that protect your position",
    icon: "🤝",
    items: [
      { id: "8-1", text: "Require proof of funds or pre-approval with all offers", critical: true },
      { id: "8-2", text: "Evaluate offers on net proceeds, not just price", critical: true },
      { id: "8-3", text: "Negotiate inspection period length (target 10-15 days)", critical: false },
      { id: "8-4", text: "Negotiate earnest money (target 1-3% hard day 1)", critical: true },
      { id: "8-5", text: "Review contingencies: financing, inspection, 1031 exchange", critical: false },
      { id: "8-6", text: "Counter or accept best offer, execute contract", critical: true },
    ],
  },
  {
    id: 9,
    title: "Due Diligence Support",
    description: "Keep the deal alive through the buyer's inspection period",
    icon: "🔬",
    items: [
      { id: "9-1", text: "Provide all requested docs within 48 hours", critical: true },
      { id: "9-2", text: "Coordinate property access for inspections and appraisal", critical: true },
      { id: "9-3", text: "Respond to buyer repair requests strategically (credit vs. repair)", critical: false },
      { id: "9-4", text: "Track contingency removal deadlines daily", critical: true },
      { id: "9-5", text: "Confirm buyer's lender appraisal is ordered", critical: false },
      { id: "9-6", text: "Maintain communication with tenants regarding access", critical: false },
    ],
  },
  {
    id: 10,
    title: "Closing & Transition",
    description: "Close smoothly and set up the buyer for success",
    icon: "🎉",
    items: [
      { id: "10-1", text: "Review HUD-1 / ALTA settlement statement 48 hours before closing", critical: true },
      { id: "10-2", text: "Notify all tenants of ownership change in writing (FL Statute 83.50)", critical: true },
      { id: "10-3", text: "Transfer security deposits to buyer at closing", critical: true },
      { id: "10-4", text: "Provide keys, codes, and vendor contacts to buyer", critical: false },
      { id: "10-5", text: "Reconcile prorated rents and deposits on closing statement", critical: true },
      { id: "10-6", text: "Retain closing docs for tax purposes (7 years)", critical: false },
    ],
  },
];
