

// Toggle special characters (single/double quotes; ampersand)
//  with special codes
// WARNING: don't use with transcription

const ampersandRegex = /&(?!\w+;)/,
      aposRegEx = /'/g,
      quotRegEx = /"/g,
      aposRegEx_reverse = /\[APOS]/g,
      quotRegEx_reverse = /\[QUOT]/g,
      ampersandRegex_reverse = /\[AMP]/g,
      inlineCssRegex = /\s+style="[^"]*"/g;

function cleanString(str) {
  if (typeof str !== 'string') {
    return '';
  } else {
    return str.replace(aposRegEx, '[APOS]')
    .replace(quotRegEx, '[QUOT]')
    .replace(ampersandRegex, '[AMP]')
    .replace(inlineCssRegex,'');
  }
}

function uncleanString(str) {
  return str.replace(aposRegEx_reverse, "'")
            .replace(quotRegEx_reverse, '"')
            .replace(ampersandRegex_reverse, '&amp;');
}

export { cleanString, uncleanString }