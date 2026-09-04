.PHONY: install install-codex install-home-codex install-home-codex-minimal install-home-codex-core help test install-antigravity install-home-antigravity

help:
	@echo "Agentic Architecture Pattern - Antigravity & Codex Configurations"
	@echo ""
	@echo "Available Targets:"
	@echo "  make install              DEST=/path/to/project  - Installs default (.agent) configs (Core 7)"
	@echo "  make install-antigravity  DEST=/path/to/project  - Installs Antigravity (.antigravity) configs"
	@echo "  make install-home-antigravity                    - Installs Antigravity configs to Home (~/.gemini/config/ & ~/.gemini/antigravity-cli/)"
	@echo "  make install-codex        DEST=/path/to/project  - Installs Codex (.codex) configs (Core 7)"
	@echo "  make install-home-codex-core                     - Installs Codex core configs to Home (~/.codex/) with AGENTS.md + skills + report-contract"
	@echo "  make install-home-codex                          - Installs Codex configs to Home (~/.codex/) with agents"
	@echo "  make install-home-codex-minimal                  - Installs Codex minimal configs to Home (~/.codex/)"
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
	mkdir -p "$$DEST_ABS/.antigravity/workflows" "$$DEST_ABS/.antigravity/skills" "$$DEST_ABS/.antigravity/templates" "$$DEST_ABS/.antigravity/tools"; \
	cp -f .antigravity/ANTIGRAVITY.md "$$DEST_ABS/.antigravity/"; \
	cp -f .antigravity/GEMINI.md "$$DEST_ABS/.antigravity/"; \
	cp -f .antigravity/GEMINI.md "$$DEST_ABS/"; \
	cp -f .antigravity/hooks.json "$$DEST_ABS/.antigravity/"; \
	cp -Rf .antigravity/workflows/ "$$DEST_ABS/.antigravity/workflows/"; \
	cp -Rf .antigravity/skills/ "$$DEST_ABS/.antigravity/skills/"; \
	cp -Rf templates/ "$$DEST_ABS/.antigravity/templates/"; \
	cp -Rf tools/ "$$DEST_ABS/.antigravity/tools/"; \
	echo "Installation complete. Target project is now ready for Antigravity."

install-home-antigravity:
	@echo "Installing Antigravity configs to Home..."
	@echo "1. Installing skills to $(HOME)/.gemini/config/skills/..."
	@mkdir -p "$(HOME)/.gemini/config/skills"
	@cp -Rf .antigravity/skills/ "$(HOME)/.gemini/config/skills/"
	@echo "2. Installing skills to $(HOME)/.gemini/antigravity-cli/skills/..."
	@mkdir -p "$(HOME)/.gemini/antigravity-cli/skills"
	@cp -Rf .antigravity/skills/ "$(HOME)/.gemini/antigravity-cli/skills/"
	@echo "3. Installing GEMINI.md and hooks.json to $(HOME)/.gemini/config/..."
	@cp -f .antigravity/GEMINI.md "$(HOME)/.gemini/config/"
	@cp -f .antigravity/hooks.json "$(HOME)/.gemini/config/"
	@echo "Home installation complete. Antigravity is now globally configured with skills, rules, and hooks."

