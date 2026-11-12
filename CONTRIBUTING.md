# Contributing

## Before contributing

Before making any changes:

- Check [issues](https://github.com/Pikachannel/reply-bots/issues) and [pull requests](https://github.com/Pikachannel/reply-bots/pulls) to see whether your idea has already been discussed or is being worked on.
- For major changes or new features, open an issue first to discuss their necessity and viability.
- Make sure you understand the contribution guidelines before submitting your changes.

## Reporting bugs & suggesting features

- **Bugs:** Open a GitHub issue using the bug report template. 
- **Security vulnerabilities:** Follow the reporting instructions in [SECURITY.md](SECURITY.md) instead of opening a public issue.
- **Feature requests:** Open a GitHub issue using the feature request template. Please allow time for me to evaluate the idea before starting work on a pull request.

## Making contributions

To submit a contribution:

1. Fork the repository.
2. Make your changes.
3. Test your changes where possible.
    - Make sure they work as intended.
    - Make sure they do not negatively affect existing bot functionality.
4. Use clear, concise commit messages.
5. Open a pull request against the project's `main` branch and fill out the provided template.

A contribution could include:

- Bug fixes
- New features
- Code improvements
- Documentation changes
- Translations into another language

## Contribution guidelines

### Code guidelines

When contributing code:

- Keep changes consistent with the project's structure.
- Prefer clear, readable, and maintainable code.
- Avoid unnecessary dependencies or APIs.
- Handle errors in a similar manner to the rest of the project.
- Avoid massive changes unless they have been discussed beforehand.
- Update documentation when your changes make the current documentation outdated.

### Translation guidelines

If you would like to translate the bot into a different language, please:

- Translate the appropriate files, including:
  - `README.md` (as e.g. `README_JA.md`)
  - The contents of `locales.json`
  - The contents of `messages.json`
- Make sure your translations are accurate and appropriate.
- Translations should preserve the original formatting.

**Translation resource:** Use the [README translation template](templates/README.md) when creating new language translations.

### Generative AI usage

**Prohibited usage:**

1. AI-generated code that the contributor:
   - Does not understand
   - Has not reviewed for security, performance, or readability
   - Has not tested themselves
2. AI-generated translations.
3. AI-generated writing, including:
   - Documentation
   - `messages.json` or `locales.json`
   - Pull requests or issues
   - Commit messages

**Disclosure requirements:**

If you use generative AI tools, you must disclose:

- **Which tools were used** (e.g., ChatGPT, Gemini, or Claude).
- **How they were used**, including which parts of the contribution they assisted with.

Contributors are responsible for what they submit, regardless of which tools they use.

### Privacy and security

Ensure that any code handling account credentials or user data does so securely and respects user privacy.

Please:
- Never commit credentials, passwords, API keys, or session tokens.
- Avoid logging sensitive information.
- Avoid collecting or storing unnecessary user data.
- Make sure you follow the privacy policy outlined in [README.md](README.md).