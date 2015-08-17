;;; xdt99-mode: xdt99 major modes for Emacs - Version 1.0.1

;; Copyright (c) 2015 Ralph Benzinger <xdt99dev@gmail.com>

;; This program is part of the TI 99 Cross-Development Tools (xdt99).

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program; if not, see <http://www.gnu.org/licenses/>.


;;; TMS 9900 Assembly

;; syntax highlighting

(defvar asm99-opcodes
  '(; 6. arithmetic
    "A" "AB" "ABS" "AI" "DEC" "DECT" "DIV" "INC" "INCT" "MPY" "NEG" "S" "SB"
    ; 7. jump and branch
    "B" "BL" "BLWP" "JEQ" "JGT" "JHE" "JH" "JL" "JLE" "JLT" "JMP" "JNC" "JNE"
    "JNO" "JOP" "JOC" "RTWP" "X" "XOP"
    ; 8. compare instructions
    "C" "CB" "CI" "COC" "CZC"
    ; 9. control and cru instructions
    "LDCR" "SBO" "SBZ" "STCR" "TB" "CKOF" "CKON" "IDLE" "RSET" "LREX"
    ; 10. load and move instructions
    "LI" "LIMI" "LWPI" "MOV" "MOVB" "STST" "STWP" "SWPB"
    ; 11. logical instructions
    "ANDI" "ORI" "XOR" "INV" "CLR" "SETO" "SOC" "SOCB" "SZC" "SZCB"
    ; 12. shift instructions
    "SRA" "SRL" "SLA" "SRC"
    ; 13. pseudo ops
    "NOP" "RT"))

(defvar asm99-directives
  '(; 14. directives
    "DEF" "REF" "EQU" "EVEN" "BSS" "BES" "COPY" "END" "DATA" "BYTE" "TEXT"
    "AORG" "RORG" "DORG" "PSEG" "PEND" "CSEG" "CEND" "DSEG" "DEND"
    "IDT" "UNL" "LIST" "PAGE" "TITL" "DXOP" "LOAD" "SREF" "END"
    ; xdt99 extensions
    "IBYTE"))

(defvar asm99-preprocessor
  '(".IFDEF" ".IFNDEF" ".IFEQ" ".IFNE" ".IFGT" ".IFGE" ".ELSE" ".ENDIF"))

(defvar asm99-font-lock-keywords
  `(
    ("^\\*.*\\|;.*" . font-lock-comment-face)
    ("'[^']*'" . font-lock-string-face)
    ("\"[^\"]*\"" . font-lock-string-face)
    ( ,(regexp-opt asm99-opcodes 'words) . font-lock-keyword-face)
    ( ,(regexp-opt asm99-directives 'words) . font-lock-builtin-face)
    ( ,(regexp-opt asm99-preprocessor 'words) . font-lock-preprocessor-face)
    (">[0-9A-F]+\\>\\|\\<[0-9]+\\>" . font-lock-constant-face)
    ("@[A-Za-z0-9_.]+" . font-lock-variable-name-face)
    ("\\<R[0-9]\\>\\|\\<R1[0-5]\\>" . font-lock-doc-face)
    ))

(setq asm99-keywords-regex
      (regexp-opt (append asm99-opcodes asm99-directives asm99-preprocessor) 'words))

;; intendation and tab key navigation

(defun asm99-indent-line ()
  "Indent left of point, but move right of point to next tab stop."
  (if asm99-smart-tab-mode (asm99-flush-left))
  (tab-to-tab-stop))

(defun asm99-flush-left ()
  "Auto-indent the current line based on left of point."
  (let* ((savep (point))
	 (indent (condition-case nil
		     (save-excursion
		       (forward-line 0)
		       (skip-chars-forward " \t")
		       (if (>= (point) savep)
			   (progn (setq savep nil) 0)
			 (max (asm99-calculate-indentation) 0)))
		   (error 0))))
    (if savep
	(save-excursion (indent-line-to indent))
      (indent-line-to indent))))

(defun asm99-calculate-indentation ()
  (or
   ; flush non-instructions to left margin
   (and (looking-at "\\w") (not (looking-at asm99-keywords-regex)) 0)
   ; flush * comments to left margin
   (and (looking-at "\\*") 0)
   ; flush everything else to first tab stop
   (or (indent-next-tab-stop 0))))

; default tab stops, customize using "M-x edit-tabs-stops"
(defvar asm99-field-positions
  '(7 12 30 60 61))

;; backspace key navigation

(defun asm99-backspace ()
  "Backspace moves cursor to end of previous field or beginning of current field if blank."
  (interactive)
  (let ((field (asm99-current-field-to-point)))
    (let ((count (length field)))
      (let ((force-del t))
	(while (and (> count 0) (or (= (preceding-char) ?\s) force-del))
	  (backward-delete-char-untabify 1)
	  (setq count (1- count))
	  (setq force-del nil))))))

(defun asm99-current-field-to-point ()
  (let ((bol (line-beginning-position)))
    (let ((tabpos (mapcar (apply-partially '+ bol) (butlast tab-stop-list))))
      (let ((start (asm99-find-largest-below (point) tabpos 1)))
	(buffer-substring-no-properties start (point))))))

(defun asm99-find-largest-below (threshold values result)
  (let ((head (car values)))
    (if (and head (< head threshold))
	(asm99-find-largest-below threshold (cdr values) head)
      result)))


;; commenter

(defvar asm99-keymap
  (let ((map (make-sparse-keymap)))
    (define-key map "\C-c;" 'comment-region)
    map)
  "Keymap for asm99-mode.")


;; major and minor mode definitions

(define-minor-mode asm99-smart-tab-mode
  "Smart tab key handling for asm99-mode"
  nil " SmartTab")

(define-minor-mode asm99-smart-backspace-mode
  "Smart backspace key handling for asm99-mode"
  nil " SmartBack" '(([backspace] . asm99-backspace)))

(defvar asm99-mode-hook nil)

(define-derived-mode asm99-mode prog-mode "asm99"
  "Major mode for editing TMS 9900 assembly source files"
  (interactive)
  ;; syntax highlighting
  (setq-local font-lock-defaults (list asm99-font-lock-keywords t t))
  ;; intendation
  (setq-local tab-stop-list asm99-field-positions)
  (setq-local indent-line-function 'asm99-indent-line)
  (setq-local indent-tabs-mode nil)
  ;; comments
  (use-local-map asm99-keymap)
  (set (make-local-variable 'comment-start) ";")
  (set (make-local-variable 'comment-padding) "")
  (set (make-local-variable 'comment-style) 'plain)
  ;; enable smart minor modes by default
  (asm99-smart-tab-mode 1)
  (asm99-smart-backspace-mode 1)
  ;; run user hooks
  (run-hooks 'asm99-mode-hook))

(provide 'asm99-mode)


;;; TI BASIC and TI Extended BASIC

;; syntax highlighting

(defvar basic99-statements
  '("ACCEPT" "ALL" "AND" "APPEND" "AT" "BASE" "BEEP" "BREAK" "CALL" "CLOSE" "DATA" "DEF"
    "DELETE" "DIGIT" "DIM" "DISPLAY" "ELSE" "END" "ERASE" "ERROR" "FIXED" "FOR"
    "GO" "GOSUB" "GOTO" "IF" "IMAGE" "INPUT" "INTERNAL" "LET" "LINPUT" "NEXT" "NOT"
    "NUMERIC" "ON" "OPEN" "OPTION" "OR" "OUTPUT" "PERMANENT" "PRINT" "RANDOMIZE"
    "READ" "RELATIVE" "REM" "RESTORE" "RETURN" "RUN" "SEQUENTIAL" "SIZE" "STEP" "STOP" "SUB"
    "SUBEND" "SUBEXIT" "THEN" "TO" "TRACE" "UALPHA" "UNBREAK" "UNTRACE" "UPDATE" "USING"
    "VALIDATE" "VARIABLE" "WARNING" "XOR"))

(defvar basic99-functions
  '("ABS" "ASC" "ATN" "COS" "EOF" "EXP" "INT" "LEN" "LOG" "MAX" "MIN" "POS" "REC"
    "RND" "SGN" "SIN" "SQR" "TAB" "TAN" "VAL"
    "CHR$" "RPT$" "SEG$" "STR$"
    "PI" "RND"))

(defvar basic99-subprograms
  '("CHAR" "CHARPAT" "CHARSET" "CLEAR" "COINC" "COLOR" "DELSPRITE" "DISTANCE"
    "ERR" "GCHAR" "HCHAR" "INIT" "JOYST" "KEY" "LINK" "LOAD" "LOCATE" "MAGNIFY"
    "MOTION" "PATTERN" "PEEK" "POSITION" "SAY" "SCREEN" "SOUND" "SPGET" "SPRITE"
    "VCHAR" "VERSION"))

(defvar basic99-commands
  '("BYE" "CON" "CONTINUE" "LIST" "MERGE" "NEW" "NUM" "NUMBER" "OLD" "RES"
    "RESEQUENCE" "SAVE"))

(defvar basic99-font-lock-keywords
  `(
    ("\"[^\"]*\"" . font-lock-string-face)
    ; line number definitions
    ("^[0-9]+" . font-lock-constant-face)            
    ("!.*\\|\\<REM .*" . font-lock-comment-face)
    ( ,(regexp-opt basic99-statements 'words) . font-lock-keyword-face)
    ( ,(regexp-opt basic99-subprograms 'words) . font-lock-builtin-face)
    ( ,(regexp-opt basic99-functions 'words) . font-lock-function-name-face)
    ( ,(regexp-opt basic99-commands 'words) . font-lock-warning-face)
    ; numbers (line number references and float literals)
    ("\\<[0-9.]+\\(?:E[-+]?[0-9]+\\)?\\>" . font-lock-variable-name-face)
    ))

;; major and minor mode definitions

(defvar basic99-mode-hook nil)

(define-derived-mode basic99-mode prog-mode "basic99"
  "Major mode for editing TI BASIC and TI Extended BASIC source files"
  (interactive)
  ;; syntax highlighting
  (setq-local font-lock-defaults (list basic99-font-lock-keywords t t))
  ;; indentation
  (setq-local indent-tabs-mode nil)
  ;; run user hooks
  (run-hooks 'basic99-mode-hook))

(provide 'basic99-mode)
