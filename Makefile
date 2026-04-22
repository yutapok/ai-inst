.PHONY: install install-claude install-codex install-home-claude install-home-codex install-home-codex-minimal help test

help:
	@echo "Agentic Architecture Pattern - Antigravity Configurations"
	@echo ""
	@echo "Available Targets:"
	@echo "  make install              DEST=/path/to/project  - Installs default (.agent) configs"
	@echo "  make install-claude       DEST=/path/to/project  - Installs Claude Code (.claude) configs"
	@echo "  make install-home-claude                         - Installs Claude Code configs to Home (~/.claude/)"
	@echo "  make install-codex        DEST=/path/to/project  - Installs Codex (.codex) configs"
	@echo "  make install-home-codex                          - Installs Codex configs to Home (~/.codex/) with prompts for compatibility"
	@echo "  make install-home-codex-minimal                  - Installs Codex configs to Home (~/.codex/) without prompts"
	@echo ""
	@echo "Example:"
	@echo "  make install-home-claude"

test:
	@python3 -m unittest discover -s tests/integration -v

install:
	@if [ -z "$(DEST)" ]; then \
		echo "Error: DEST variable is required."; \
		echo "Usage: make install DEST=/path/to/target/project"; \
		exit 1; \
	fi
	@DEST_ABS=$$(realpath "$(DEST)" 2>/dev/null || echo ""); \
	if [ -z "$$DEST_ABS" ]; then echo "Error: DEST path '$(DEST)' is not resolvable."; exit 1; fi; \
	if [ -d "$$DEST_ABS/.agent" ] && [ -z "$(FORCE)" ]; then \
		echo "Warning: $$DEST_ABS/.agent already exists. Use FORCE=1 to overwrite."; exit 1; \
	fi; \
	echo "Installing .agent to $$DEST_ABS..."; \
	mkdir -p "$$DEST_ABS"; \
	cp -R .agent "$$DEST_ABS/"; \
	echo "Installation complete. Target project is now ready for Antigravity (.agent)."

install-claude:
	@if [ -z "$(DEST)" ]; then \
		echo "Error: DEST variable is required."; \
		echo "Usage: make install-claude DEST=/path/to/target/project"; \
		exit 1; \
	fi
	@DEST_ABS=$$(realpath "$(DEST)" 2>/dev/null || echo ""); \
	if [ -z "$$DEST_ABS" ]; then echo "Error: DEST path '$(DEST)' is not resolvable."; exit 1; fi; \
	if [ -d "$$DEST_ABS/.claude" ] && [ -z "$(FORCE)" ]; then \
		echo "Warning: $$DEST_ABS/.claude already exists. Use FORCE=1 to overwrite."; exit 1; \
	fi; \
	echo "Installing .claude to $$DEST_ABS..."; \
	mkdir -p "$$DEST_ABS"; \
	cp -R .claude "$$DEST_ABS/"; \
	echo "Installation complete. Target project is now ready for Claude Code."

install-home-claude:
	@echo "Installing Claude Code configs to $(HOME)/.claude/..."
	@mkdir -p "$(HOME)/.claude/commands" "$(HOME)/.claude/skills"
	@cp -f .claude/CLAUDE.md "$(HOME)/.claude/"
	@cp -Rf .claude/commands/ "$(HOME)/.claude/commands/"
	@cp -Rf .claude/skills/ "$(HOME)/.claude/skills/"
	@echo "Home installation complete. Claude Code is now globally configured with Antigravity."

install-codex:
	@if [ -z "$(DEST)" ]; then \
		echo "Error: DEST variable is required."; \
		echo "Usage: make install-codex DEST=/path/to/target/project"; \
		exit 1; \
	fi
	@DEST_ABS=$$(realpath "$(DEST)" 2>/dev/null || echo ""); \
	if [ -z "$$DEST_ABS" ]; then echo "Error: DEST path '$(DEST)' is not resolvable."; exit 1; fi; \
	if [ -d "$$DEST_ABS/.codex" ] && [ -z "$(FORCE)" ]; then \
		echo "Warning: $$DEST_ABS/.codex already exists. Use FORCE=1 to overwrite."; exit 1; \
	fi; \
	echo "Installing .codex to $$DEST_ABS..."; \
	mkdir -p "$$DEST_ABS"; \
	cp -R .codex "$$DEST_ABS/"; \
	echo "Installation complete. Target project is now ready for Codex."

install-home-codex:
	@echo "Installing Codex configs to $(HOME)/.codex/..."
	@mkdir -p "$(HOME)/.codex/prompts" "$(HOME)/.codex/skills" "$(HOME)/.codex/agents"
	@cp -f .codex/AGENTS.md "$(HOME)/.codex/"
	@cp -Rf .codex/prompts/ "$(HOME)/.codex/prompts/"
	@cp -Rf .codex/skills/ "$(HOME)/.codex/skills/"
	@cp -Rf .codex/agents/ "$(HOME)/.codex/agents/"
	@echo "Home installation complete. Codex is now globally configured with Antigravity (AGENTS.md + skills + agents, plus prompts for compatibility)."

install-home-codex-minimal:
	@echo "Installing minimal Codex configs to $(HOME)/.codex/..."
	@mkdir -p "$(HOME)/.codex/skills" "$(HOME)/.codex/agents"
	@cp -f .codex/AGENTS.md "$(HOME)/.codex/"
	@cp -Rf .codex/skills/ "$(HOME)/.codex/skills/"
	@cp -Rf .codex/agents/ "$(HOME)/.codex/agents/"
	@echo "Minimal home installation complete. Codex is now globally configured with Antigravity (AGENTS.md + skills + agents)."
