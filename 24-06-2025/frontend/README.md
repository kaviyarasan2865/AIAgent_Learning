# Agentic AI Bug Fixer - Frontend

A modern, intuitive web interface for the Agentic AI-Based Bug Fixer system. This frontend provides a seamless user experience for uploading code, viewing AI analysis results, and managing the approval workflow.

## Features

### 🎨 Modern UI/UX Design
- **Glassmorphism Design**: Beautiful backdrop blur effects and modern card layouts
- **Dark Mode Support**: Automatic dark/light mode detection with smooth transitions
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Smooth Animations**: Subtle animations and transitions for better user experience

### 🤖 AI Agent Workflow Visualization
- **Real-time Agent Status**: Live tracking of each AI agent's processing status
- **Workflow Progress**: Visual progress indicator showing current step in the analysis
- **Agent Dashboard**: Detailed view of each agent's role and current status

### 📊 Enhanced Code Analysis
- **Side-by-side Code Comparison**: Before/after code comparison with syntax highlighting
- **Issue Categorization**: Issues organized by type (layout, content, JavaScript, etc.)
- **Severity Indicators**: Color-coded severity levels for different issues
- **Fix Previews**: Detailed preview of proposed fixes with explanations

### ✅ Approval Workflow
- **Interactive Approval Dashboard**: Comprehensive review interface for proposed changes
- **Selective Approval**: Choose which fixes to apply
- **Audit Trail**: Complete history of all actions and decisions
- **Summary Statistics**: Overview of fixes, optimizations, and manual interventions

### 📁 File Upload Support
- **Drag & Drop**: Easy file upload for HTML, CSS, and JavaScript files
- **Code Pasting**: Direct code input with syntax highlighting
- **File Validation**: Automatic file type detection and validation

## Technology Stack

- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS 4 with custom design system
- **TypeScript**: Full type safety and better developer experience
- **Icons**: Lucide React for consistent iconography
- **Utilities**: clsx and tailwind-merge for better class management

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles and design tokens
│   ├── layout.tsx         # Root layout component
│   └── page.tsx           # Main application page
├── components/            # Reusable UI components
│   ├── AgentStatus.tsx    # AI agent status dashboard
│   ├── ApprovalDashboard.tsx # User approval interface
│   ├── AuditLog.tsx       # Audit trail component
│   ├── CodeComparison.tsx # Side-by-side code comparison
│   ├── CodeUpload.tsx     # File upload and code input
│   ├── FixPreview.tsx     # Fix suggestions display
│   ├── IssueReport.tsx    # Issue detection results
│   └── WorkflowProgress.tsx # Workflow progress indicator
└── lib/                   # Utility functions
    └── utils.ts           # Common utility functions
```

## Key Components

### WorkflowProgress
Visual progress indicator showing the 6-step AI analysis workflow:
1. Upload Code
2. AI Analysis  
3. Issue Detection
4. Fix Generation
5. User Approval
6. Complete

### AgentStatus
Real-time dashboard showing the status of each AI agent:
- **Layout Validator**: Detects layout and responsiveness issues
- **Content Healer**: Identifies broken content and placeholders
- **Fix Generator**: Generates intelligent code fixes
- **Code Optimizer**: Applies RAG-based optimizations
- **User Approval**: Prepares approval dashboard

### CodeComparison
Side-by-side comparison tool with:
- Tabbed interface for HTML, CSS, and JavaScript
- Syntax highlighting
- Change indicators
- Before/after code views

### ApprovalDashboard
Comprehensive review interface featuring:
- Summary statistics
- Fix previews
- Manual intervention requirements
- Approval/rejection actions

## Design System

The frontend uses a comprehensive design system with:

### Color Palette
- **Primary**: Blue (#2563eb) for main actions and branding
- **Success**: Green (#10b981) for positive states
- **Warning**: Amber (#f59e0b) for caution states  
- **Error**: Red (#ef4444) for error states
- **Neutral**: Slate grays for text and backgrounds

### Typography
- **Headings**: Bold, hierarchical typography
- **Body**: Readable sans-serif fonts
- **Code**: Monospace fonts for code blocks

### Spacing & Layout
- **Consistent spacing**: 4px base unit system
- **Responsive grid**: Flexible layouts that adapt to screen size
- **Card-based design**: Content organized in clean, bordered cards

## API Integration

The frontend integrates with the backend API endpoints:

- `POST /api/bug-fix` - Submit code for analysis
- `POST /api/approval/{id}` - Submit approval decision
- `GET /api/audit-logs/{id}` - Fetch audit trail

## Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for all new components
3. Add proper error handling and loading states
4. Test responsive behavior across different screen sizes
5. Ensure accessibility standards are met

## License

This project is part of the Agentic AI Bug Fixer system.
