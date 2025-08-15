import React from "react";

export const FormatHelpContent = () => (
  <div>
    <p>Use these markup tags to format your resume content:</p>

    <p>
      <strong>Bold text:</strong>
    </p>
    <p>
      <code>&lt;b&gt;your text&lt;/b&gt;</code>
    </p>

    <p>
      <strong>Italic text:</strong>
    </p>
    <p>
      <code>&lt;i&gt;your text&lt;/i&gt;</code>
    </p>

    <p>
      <strong>Hyperlinks:</strong>
    </p>
    <p>
      <code>
        &lt;a href="https://example.com" color="blue"&gt;Link Text&lt;/a&gt;
      </code>
    </p>

    <p>
      <strong>Example:</strong>
    </p>
    <p>
      <code>
        Developed &lt;b&gt;React applications&lt;/b&gt; for &lt;a
        href="https://github.com" color="blue"&gt;GitHub&lt;/a&gt;
      </code>
    </p>

    <p>
      <strong>Advanced Formatting:</strong> Your text is basically treated as
      RML, which is basically HTML but more cringe. Feel free to use other tags
      to achieve specific appearance.
    </p>

    <p>
      <strong>Note:</strong> These markup tags only appear when editing in Edit
      Mode. In View Mode and Parameters Mode, you'll see the clean formatted
      text without the markup tags. To add or modify formatting, switch to Edit
      Mode.
    </p>
  </div>
);

export const ModeHelpContent = () => (
  <div>
    <p>Choose the right mode for your current task:</p>

    <ul>
      <li>
        <strong>View Mode:</strong> Clean preview of your resume without any
        markup tags. Perfect for reviewing how your resume will look to
        employers. Note: markup tags won't show up here, but they will in resume
      </li>
      <li>
        <strong>Edit Mode:</strong> Full editing capabilities with ReportLab
        markup support. Add content, format text with markup, and arrange your
        resume.
      </li>
      <li>
        <strong>Parameters Mode:</strong> Fine-tune AI optimization settings.
        Adjust weights and bias base on your opinion on the app's item selection
        decisions. Higher weight & bias means more likely to be included in
        tailored resumes.
      </li>
    </ul>

    <p>
      <strong>Tip:</strong> Use Edit Mode to build your content, View Mode to
      review the final appearance, and Parameters Mode to optimize for specific
      job applications.
    </p>
  </div>
);
