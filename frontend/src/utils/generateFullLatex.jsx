const escapeLatex = (str) => {
  if (!str) return "";
  return str
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/([%#&_{}$^~])/g, "\\$1");
};

export const generateLatexHeader = (headingInfo) => {
  const { heading_name, subsequent_content } = headingInfo;

  // Format each contact item with proper LaTeX formatting
  const formattedContent = subsequent_content.map((item) => {
    const escapedItem = escapeLatex(item);
    if (item.includes("@")) {
      // Email formatting
      return `\\href{mailto:${item}}{\\underline{${escapedItem}}}`;
    } else if (item.includes("github.com")) {
      // GitHub link formatting
      return `\\href{${item}}{\\underline{${escapedItem
        .replace("https://", "")
        .replace("github.com/", "github.com/")}}}`;
    } else if (item.includes("linkedin.com")) {
      // LinkedIn formatting
      return `\\href{${item}}{\\underline{${escapedItem.replace(
        "https://",
        ""
      )}}}`;
    } else {
      // Phone numbers and other content
      return escapedItem;
    }
  });

  return `\\begin{center}
    \\textbf{\\Huge \\scshape ${escapeLatex(heading_name)}} \\\\ \\vspace{1pt}
    \\small ${formattedContent.join(" $|$ ")}
\\end{center}`;
};

export const generateLatexSection = (section) => {
  const escapedSectionTitle = escapeLatex(section.title);
  return `\\section{${escapedSectionTitle}}
  \\resumeSubHeadingListStart
    ${section.items.map(generateLatexItem).join("\n")}
  \\resumeSubHeadingListEnd`;
};

export const generateLatexItem = (item) => {
  const titles = item.titles.filter((title) => title.trim());
  if (titles.length === 0) {
    const lines = item.lines
      .map((line) => `        \\item{${escapeLatex(line.content_str)}}`)
      .join("\n");

    return `
      \\begin{itemize}
        ${lines}
      \\end{itemize}`;
  }
  // Split titles into position and date, organization and location
  const position = escapeLatex(titles[0]) || "";
  const date = escapeLatex(titles[1]) || "";
  const organization = escapeLatex(titles[2]) || "";
  const location = escapeLatex(titles[3]) || "";

  const lines = item.lines
    .map((line) => `        \\resumeItem{${escapeLatex(line.content_str)}}`)
    .join("\n");

  return `    \\resumeSubheading
      {${position}}{${organization}}
      {${date}}{${location}}
      \\resumeItemListStart
${lines}
      \\resumeItemListEnd`;
};

export const generateFullLatex = (resumeData) => {
  const documentClass = `\\documentclass[letterpaper,11pt]{article}

\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{fancyhdr}
\\usepackage[english]{babel}
\\usepackage{tabularx}
\\input{glyphtounicode}

\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.5in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1.0in}

\\urlstyle{same}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
  \\vspace{-4pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\\pdfgentounicode=1

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[1]{
  \\item\\small{
    {#1 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubSubheading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\textit{\\small#1} & \\textit{\\small #2} \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeProjectHeading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\small#1 & #2 \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}

\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

\\begin{document}`;

  const header = generateLatexHeader(resumeData.heading_info);
  const sections = resumeData.sections.map(generateLatexSection).join("\n\n");

  return `${documentClass}

${header}

${sections}

\\end{document}`;
};
