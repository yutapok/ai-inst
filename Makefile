.PHONY: install install-claude install-codex install-home-claude install-home-codex install-home-codex-minimal install-home-codex-core help test install-antigravity install-home-antigravity

help:
	@echo "Agentic Architecture Pattern - Antigravity Configurations"
	@echo ""
	@echo "Available Targets:"
	@echo "  make install              DEST=/path/to/project  - Installs default (.agent) configs"
	@echo "  make install-antigravity  DEST=/path/to/project  - Installs Antigravity (.antigravity) configs"
	@echo "  make install-home-antigravity                    - Installs Antigravity configs to Home (~/.gemini/config/skills/ & ~/.gemini/antigravity-cli/skills/)"
	@echo "  make install-claude       DEST=/path/to/project  - Installs Claude Code (.claude) configs"
	@echo "  make install-home-claude                         - Installs Claude Code configs to Home (~/.claude/)"
	@echo "  make install-codex        DEST=/path/to/project  - Installs Codex (.codex) configs"
	@echo "  make install-home-codex-core                     - Installs Codex core configs to Home (~/.codex/) with AGENTS.md + skills + report-contract"
	@echo "  make install-home-codex                          - Installs Codex configs to Home (~/.codex/) with prompts for compatibility"
	@echo "  make install-home-codex-minimal                  - Installs Codex configs to Home (~/.codex/) without prompts"
	@echo ""
	@echo "Example:"
	@echo "  make install-home-antigravity"

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
	rm -rf "$$DEST_ABS/.claude"; \
	mkdir -p "$$DEST_ABS/.claude/commands" "$$DEST_ABS/.claude/skills" "$$DEST_ABS/.claude/agents"; \
	cp -f .claude/CLAUDE.md "$$DEST_ABS/.claude/"; \
	cp -Rf .claude/commands/ "$$DEST_ABS/.claude/commands/"; \
	cp -Rf .claude/skills/ "$$DEST_ABS/.claude/skills/"; \
	cp -Rf .claude/agents/ "$$DEST_ABS/.claude/agents/"; \
	echo "Installation complete. Target project is now ready for Claude Code."

install-home-claude:
	@echo "Installing Claude Code configs to $(HOME)/.claude/..."
	@rm -f "$(HOME)/.claude/CLAUDE.md"
	@rm -rf "$(HOME)/.claude/commands" "$(HOME)/.claude/skills" "$(HOME)/.claude/agents"
	@mkdir -p "$(HOME)/.claude/commands" "$(HOME)/.claude/skills"
	@cp -f .claude/CLAUDE.md "$(HOME)/.claude/"
	@cp -Rf .claude/commands/ "$(HOME)/.claude/commands/"
	@cp -Rf .claude/skills/ "$(HOME)/.claude/skills/"
	@cp -Rf .claude/agents/ "$(HOME)/.claude/agents/"
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
	rm -rf "$$DEST_ABS/.codex"; \
	mkdir -p "$$DEST_ABS/.codex/skills" "$$DEST_ABS/.codex/agents" "$$DEST_ABS/.codex/report-contract" "$$DEST_ABS/.codex/reports"; \
	cp -f .codex/AGENTS.md "$$DEST_ABS/.codex/"; \
	cp -f .codex/config.toml "$$DEST_ABS/.codex/"; \
	cp -Rf .codex/skills/ "$$DEST_ABS/.codex/skills/"; \
	cp -Rf .codex/agents/ "$$DEST_ABS/.codex/agents/"; \
	cp -Rf .codex/report-contract/ "$$DEST_ABS/.codex/report-contract/"; \
	echo "Installation complete. Target project is now ready for Codex."

install-home-codex-core:
	@echo "Installing Codex core configs to $(HOME)/.codex/..."
	@rm -f "$(HOME)/.codex/AGENTS.md" "$(HOME)/.codex/config.toml"
	@rm -rf "$(HOME)/.codex/skills" "$(HOME)/.codex/agents" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@mkdir -p "$(HOME)/.codex/skills" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@cp -f .codex/AGENTS.md "$(HOME)/.codex/"
	@cp -Rf .codex/skills/ "$(HOME)/.codex/skills/"
	@cp -Rf .codex/report-contract/ "$(HOME)/.codex/report-contract/"
	@echo "Core home installation complete. Codex is now globally configured with Antigravity (AGENTS.md + skills + report-contract)."

install-home-codex:
	@echo "Installing Codex configs to $(HOME)/.codex/..."
	@rm -f "$(HOME)/.codex/AGENTS.md" "$(HOME)/.codex/config.toml"
	@rm -rf "$(HOME)/.codex/skills" "$(HOME)/.codex/agents" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@mkdir -p "$(HOME)/.codex/skills" "$(HOME)/.codex/agents" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@cp -f .codex/AGENTS.md "$(HOME)/.codex/"
	@cp -f .codex/config.toml "$(HOME)/.codex/"
	@cp -Rf .codex/skills/ "$(HOME)/.codex/skills/"
	@cp -Rf .codex/agents/ "$(HOME)/.codex/agents/"
	@cp -Rf .codex/report-contract/ "$(HOME)/.codex/report-contract/"
	@echo "Home installation complete. Codex is now globally configured with Antigravity (AGENTS.md + skills + agents + report-contract)."

install-home-codex-minimal:
	@echo "Installing minimal Codex configs to $(HOME)/.codex/..."
	@rm -f "$(HOME)/.codex/AGENTS.md" "$(HOME)/.codex/config.toml"
	@rm -rf "$(HOME)/.codex/skills" "$(HOME)/.codex/agents" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@mkdir -p "$(HOME)/.codex/skills" "$(HOME)/.codex/agents" "$(HOME)/.codex/report-contract" "$(HOME)/.codex/reports"
	@cp -f .codex/AGENTS.md "$(HOME)/.codex/"
	@cp -f .codex/config.toml "$(HOME)/.codex/"
	@cp -Rf .codex/skills/ "$(HOME)/.codex/skills/"
	@cp -Rf .codex/agents/ "$(HOME)/.codex/agents/"
	@cp -Rf .codex/report-contract/ "$(HOME)/.codex/report-contract/"
	@echo "Minimal home installation complete. Codex is now globally configured with Antigravity (AGENTS.md + skills + agents + report-contract)."

install-antigravity:
	@if [ -z "$(DEST)" ]; then \
		echo "Error: DEST variable is required."; \
		echo "Usage: make install-antigravity DEST=/path/to/target/project"; \
		exit 1; \
	fi
	@DEST_ABS=$$(realpath "$(DEST)" 2>/dev/null || echo ""); \
	if [ -z "$$DEST_ABS" ]; then echo "Error: DEST path '$(DEST)' is not resolvable."; exit 1; fi; \
	if [ -d "$$DEST_ABS/.antigravity" ] && [ -z "$(FORCE)" ]; then \
		echo "Warning: $$DEST_ABS/.antigravity already exists. Use FORCE=1 to overwrite."; exit 1; \
	fi; \
	echo "Installing .antigravity to $$DEST_ABS..."; \
	rm -rf "$$DEST_ABS/.antigravity"; \
	mkdir -p "$$DEST_ABS/.antigravity/workflows" "$$DEST_ABS/.antigravity/skills"; \
	cp -f .antigravity/ANTIGRAVITY.md "$$DEST_ABS/.antigravity/"; \
	cp -Rf .antigravity/workflows/ "$$DEST_ABS/.antigravity/workflows/"; \
	cp -Rf .antigravity/skills/ "$$DEST_ABS/.antigravity/skills/"; \
	echo "Installation complete. Target project is now ready for Antigravity."

install-home-antigravity:
	@echo "Installing Antigravity configs to Home..."
	@echo "1. Installing skills to $(HOME)/.gemini/config/skills/..."
	@mkdir -p "$(HOME)/.gemini/config/skills"
	@cp -Rf .antigravity/skills/ "$(HOME)/.gemini/config/skills/"
	@echo "2. Installing skills to $(HOME)/.gemini/antigravity-cli/skills/..."
	@mkdir -p "$(HOME)/.gemini/antigravity-cli/skills"
	@cp -Rf .antigravity/skills/ "$(HOME)/.gemini/antigravity-cli/skills/"
	@echo "Home installation complete. Antigravity is now globally configured with skills."
