.PHONY: install install-claude install-codex help

help:
	@echo "Agentic Architecture Pattern - Antigravity Configurations"
	@echo ""
	@echo "Available Targets:"
	@echo "  make install        DEST=/path/to/project  - Installs default (.agent) configs"
	@echo "  make install-claude DEST=/path/to/project  - Installs Claude Code (.claude) configs"
	@echo "  make install-codex  DEST=/path/to/project  - Installs Codex (.codex) configs"
	@echo ""
	@echo "Example:"
	@echo "  make install-claude DEST=../my-new-app"

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
