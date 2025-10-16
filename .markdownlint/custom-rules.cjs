'use strict';

module.exports = [
  {
    names: ['custom/no-closing-fence-info'],
    description: 'Closing fenced code blocks must not include an info string',
    tags: ['code', 'fence'],
    function: function customNoClosingFenceInfo(params, onError) {
      const { tokens, lines } = params;
      for (const token of tokens) {
        if (token.type !== 'fence' || !token.map || token.map.length !== 2) {
          continue;
        }
        const closingLineIndex = token.map[1] - 1;
        if (closingLineIndex < 0 || closingLineIndex >= lines.length) {
          continue;
        }
        const closingLine = lines[closingLineIndex];
        if (!closingLine) {
          continue;
        }
        const trimming = closingLine.trimStart();
        const markup = token.markup || '';
        if (!markup || !trimming.startsWith(markup)) {
          continue;
        }
        const afterMarkup = trimming.slice(markup.length);
        if (afterMarkup.trim().length === 0) {
          continue;
        }
        onError({
          lineNumber: closingLineIndex + 1,
          detail: `Closing fence must contain only "${markup}"`,
          context: closingLine.trim()
        });
      }
    }
  }
];
