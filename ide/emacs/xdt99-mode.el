;;; xdt99-mode: xdt99 major modes for Emacs - Version 1.4

;; Copyright (c) 2015-2021 Ralph Benzinger <r@0x01.de>

;; This program is part of the TI 99 Cross-Development Tools (xdt99).

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 3 of the License, or
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

(defvar asm99-foreign-opcodes
  '(; other architectures
    "MPYS" "DIVS" "LST" "LWP" "BIND" "BLSK" "TMB" "TCMB" "TSMB" "AM" "SM" "SLAM" "SRAM"
    "CALL" "RET" "PUSH" "POP" "SLC" "PIX"))

(defvar asm99-directives
  '(; 14. directives
    "DEF" "REF" "EQU" "EVEN" "BSS" "BES" "COPY" "END" "DATA" "BYTE" "TEXT"
    "AORG" "RORG" "DORG" "PSEG" "PEND" "CSEG" "CEND" "DSEG" "DEND"
    "IDT" "UNL" "LIST" "PAGE" "TITL" "DXOP" "LOAD" "SREF"
    ; xdt99 extensions
    "WEQU" "REQU" "BCOPY" "XORG" "SAVE" "BANK" "STRI" "FLOA" "AUTO"))

(defvar asm99-preprocessor
  '(".IFDEF" ".IFNDEF" ".IFEQ" ".IFNE" ".IFGT" ".IFGE" ".ELSE" ".ENDIF" ".ERROR"))

; new face for 9995/99105/F18A keywords
(defface extra-face
   '((t . (:foreground "violet red" :inherit (font-lock-keyword-face))))
   "Face for displaying foreign architecture keywords.")

; create keywords table for syntax highlighting
(defvar asm99-font-lock-keywords
  `(
    (";:.*" . font-lock-doc-face)                                               ; pragma
    ("^\\*.*\\|;.*" . font-lock-comment-face)                                   ; comment
    ("'[^']*'" . font-lock-string-face)                                         ; char literal
    ("\"[^\"]*\"" . font-lock-string-face)                                      ; string literal
    ("[BbWwSsLlXx]#" . font-lock-type-face)                                     ; # expression
    ( ,(regexp-opt asm99-opcodes 'symbols) . font-lock-keyword-face)            ; opcodes
    ( ,(regexp-opt asm99-foreign-opcodes 'symbols) . 'extra-face)               ; other architectures
    ( ,(regexp-opt asm99-directives 'symbols) . font-lock-builtin-face)         ; directives
    ( ,(regexp-opt asm99-preprocessor 'symbols) . font-lock-preprocessor-face)  ; preprocessor commands
    (">[0-9A-F]+\\>\\|\\<[0-9]+\\>" . font-lock-constant-face)                  ; numerical constants
    ("@[A-Za-z0-9_.]+" . font-lock-variable-name-face)                          ; @symbol
    ("\\_<R[0-9]\\_>\\|\\_<R1[0-5]\\_>" . font-lock-doc-face)                   ; register
    ))

; add additional characters to syntax classes (symbols '_' and punctuation '.')
(defvar asm99-syntax-table
  (let ((table (make-syntax-table))
        (symbols '(?! ?$ ?? ?@))
        (punctuations '(?: ?% ?& ?* ?+ ?- ?/ ?< ?= ?>)))
    (mapc (lambda (c) (modify-syntax-entry c "_" table)) symbols)
    (mapc (lambda (c) (modify-syntax-entry c "." table)) punctuations)
    (modify-syntax-entry ?' "\"" table)
    table))

(setq asm99-keywords-regex
      (regexp-opt (append asm99-opcodes asm99-foreign-opcodes asm99-directives asm99-preprocessor) 'symbols))

;; intendation and smart edit modes

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
   ; flush * comments to left margin
   (and (looking-at "\\*") 0)
   ; flush non-instructions to left margin
   (and (looking-at "\\w\\|\\s_") (not (looking-at asm99-keywords-regex)) 0)
   ; flush everything else to first tab stop
   (or (car tab-stop-list) 0)))

; default tab stops, customize using "M-x edit-tabs-stops"
(defvar asm99-field-positions
  '(7 12 30 37))

(defun asm99-backspace ()
  "Backspace moves cursor to end of previous field or beginning of current field if blank."
  (interactive)
  (let ((field (asm99-current-field-to-point)))
    (let ((count (length field)))
      (if (/= (preceding-char) ?\s)
          (backward-delete-char-untabify 1)
        (while (and (> count 0) (= (preceding-char) ?\s))
          (backward-delete-char-untabify 1)
          (setq count (1- count)))))))

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

;; simple navigation (also for GPL)

(defun xdt99-get-symbol (word)
  "return plain symbol without addressing mode"
  (if word
      (if (let ((prefix (substring word 0 1)))
            (or (string= prefix "@")
                (string= prefix "*")))
          (substring word 1)
          (if (let ((prefix (downcase (substring word 0 2))))
                (or (string= prefix "v@")
                    (string= prefix "v*")
                    (string= prefix "g@")))
              (substring word 2)
              word))
      nil))

(defun asm99-goto-symbol-definition ()
  "jump to label definition"
  (interactive)
  (let ((current-symbol (xdt99-get-symbol (current-word t nil))))
    (if current-symbol
        (let ((symbol-pattern (concat "^" current-symbol ":?\\s-"))
              (symbol-pos nil))
          (save-excursion
            (goto-char 1)
            (if (let ((case-fold-search t))
                  (re-search-forward symbol-pattern nil t 1))
                (setq symbol-pos (match-beginning 0))))
          (if symbol-pos
              (goto-char symbol-pos))))))

(defun asm99-show-symbol-definition ()
  "show label definition"
  (interactive)
  (let ((current-symbol (xdt99-get-symbol (current-word t nil))))
    (if current-symbol
      (let ((symbol-pattern (concat "^" current-symbol "\\(:\\)?\\s-")))
        (save-excursion
          (goto-char 1)
          (if (let ((case-fold-search t))
                (re-search-forward symbol-pattern nil t 1))
              (let ((beginning-of-text (match-beginning 0))
                    (end-of-text (line-end-position (if (match-string 1) 1 nil))))
                (message "%s" (buffer-substring beginning-of-text end-of-text)))
            (message "%s" "Symbol definition not found.")))))))

;; commenter

(defvar asm99-keymap
  (let ((map (make-sparse-keymap)))
    (define-key map "\C-c;" 'comment-region)
    map)
  "Keymap for asm99-mode.")

;; compilation

(defcustom asm99-compile-options
  "-b -R"
  "options passed to xas99")

(defun asm99-compile-command ()
    (set (make-local-variable 'compile-command)
       (concat "xas99.py " asm99-compile-options " " buffer-file-name)))

;; major and minor mode definitions

(setq face-font-selection-order
      '(:width :height :weight :slant))

(define-minor-mode asm99-smart-tab-mode
  "Smart tab key handling for asm99-mode"
  nil " SmartTab")

(define-minor-mode asm99-smart-backspace-mode
  "Smart backspace key handling for asm99-mode"
  nil " SmartBack" '(([backspace] . asm99-backspace)))

(defvar asm99-mode-hook nil)
(add-hook 'asm99-mode-hook
          (lambda ()
            (set (make-local-variable 'compile-command)
                 (asm99-compile-command))))

; default tab stops, customize using "M-x edit-tabs-stops"
(defvar asm99-field-positions
  '(7 12 30 60 61))

(define-derived-mode asm99-mode prog-mode "asm99"
  "Major mode for editing TMS 9900 assembly source files"
  (interactive)
  ;; syntax highlighting
  (set-syntax-table asm99-syntax-table)
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


;;; Graphics Programming Language (GPL)

;; syntax highlighting

(defvar gpl99-opcodes
  ;; 4.1 compare and test instructions
  '("H" "GT" "CARRY" "OVF" "CEQ" "DCEQ" "CH" "DCH" "CHE" "DCHE"
    "CGT" "DCGT" "CGE" "DCGE" "CLOG" "DCLOG" "CZ" "DCZ"
    ;; 4.2 program control instructions
    "BS" "BR" "B" "CASE" "DCASE" "CALL" "FETCH" "RTN" "RTNC"
    ;; 4.3 bit manipulation and pseudo instruction
    "RB" "SB" "TBR" "HOME" "POP"
    ;; 4.4 arithmetic and logical instructions
    "ADD" "DADD" "SUB" "DSUB" "MUL" "DMUL" "DIV" "DDIV" "INC" "DINC"
    "INCT" "DINCT" "DEC" "DDEC" "DECT" "DDECT" "ABS" "DABS" "NEG"
    "DNEG" "INV" "DINV" "AND" "DAND" "OR" "DOR" "XOR" "DXOR" "CLR"
    "DCLR" "ST" "DST" "EX" "DEX" "PUSH" "MOVE" "SLL" "DSLL" "SRA"
    "DSRA" "SRL" "DSRL" "SRC" "DSRC"
    ;; 4.5 graphics and miscellaneous instructions
    "COINC" "BACK" "ALL" "RAND" "SCAN" "XML" "EXIT" "I/O"
    ;; BASIC
    "PARSE" "CONT" "EXEC" "RTNB"
    ;; undocumented
    "SWGR" "DSWGR" "RTGR"
    ;; variants
    "IO"
    )
  )

(defvar gpl99-format
  '("FMT" "FEND" "HTEXT" "VTEXT" "HCHAR" "VCHAR" "COL+" "ROW+"
    "HMOVE" "FOR" "BIAS" "ROW" "COL"
    ;; variants RAG/RYTE DATA
    "HTEX" "VTEX" "HCHA" "VCHA" "HSTR" "SCRO" "IROW" "ICOL"
    ;; variants mizapf
    "PRINTH" "PRINTV" "TIMES" "DOWN" "RIGHT" "XGPL"
    )
  )

(defvar gpl99-directives
  '("EQU" "DATA" "BYTE" "TEXT" "BSS" "GROM" "AORG" "TITLE"
    "COPY" "END" "PAGE" "LIST" "UNL" "LISTM" "UNLM"
    ;; variants
    "ORG" "TITL" "IDT"
    ;; extensions
    "STRI" "FLOAT"
    )
  )

(defvar gpl99-preprocessor
  '(".IFDEF" ".IFNDEF" ".IFEQ" ".IFNE" ".IFGT" ".IFGE" ".ELSE" ".ENDIF" ".ERROR")
  )

(defvar gpl99-font-lock-keywords
  `(
    ("^\\*.*\\|;.*" . font-lock-comment-face)
    ("'[^']*'" . font-lock-string-face)
    ("\"[^\"]*\"" . font-lock-string-face)
    ( ,(regexp-opt gpl99-opcodes 'symbols) . font-lock-keyword-face)
    ( ,(regexp-opt gpl99-format 'symbols) . font-lock-function-name-face)
    ( ,(regexp-opt gpl99-directives 'symbols) . font-lock-builtin-face)
    ( ,(regexp-opt gpl99-preprocessor 'symbols) . font-lock-preprocessor-face)
    (">[0-9A-F]+\\>\\|\\<[0-9]+\\>" . font-lock-constant-face)
    ;("[GV]?[@*][A-Za-z0-9_.]*" . font-lock-variable-name-face)
    ("[GV]?@\\|#" . font-lock-variable-name-face)  ; only highlight addr prefix
    ("\\(V?\\*\\)[^ ]" 1 font-lock-variable-name-face)  ; only highlight addr prefix
    ))

(defvar gpl99-syntax-table
  (let ((table (make-syntax-table))
        (symbols '(?! ?$ ?: ?@))
        (punctuations '(?, ?% ?& ?* ?+ ?- ?/ ?< ?= ?>)))
    (mapc (lambda (c) (modify-syntax-entry c "_" table)) symbols)
    (mapc (lambda (c) (modify-syntax-entry c "." table)) punctuations)
    (modify-syntax-entry ?' "\"" table)
    table))

(setq gpl99-keywords-regex
      (regexp-opt (append gpl99-opcodes gpl99-format gpl99-directives gpl99-preprocessor) 'symbols))

(defvar gpl99-field-positions
  '(7 13 30 60 61))

;; compilation

(defcustom gpl99-compile-options
  "-b"
  "options passed to xga99")

(defun gpl99-compile-command ()
    (set (make-local-variable 'compile-command)
       (concat "xga99.py " gpl99-compile-options " " buffer-file-name)))

;; major and minor mode definitions

(define-minor-mode gpl99-smart-tab-mode
  "Smart tab key handling for gpl99-mode"
  nil " SmartTab")

(define-minor-mode gpl99-smart-backspace-mode
  "Smart backspace key handling for gpl99-mode"
  nil " SmartBack" '(([backspace] . asm99-backspace)))

(defvar gpl99-mode-hook nil)
(add-hook 'gpl99-mode-hook
          (lambda ()
            (set (make-local-variable 'compile-command)
                 (gpl99-compile-command))))

(define-derived-mode gpl99-mode prog-mode "gpl99"
  "Major mode for editing GPL source files"
  (interactive)
  ;; syntax highlighting
  (set-syntax-table gpl99-syntax-table)
  (setq-local font-lock-defaults (list gpl99-font-lock-keywords t t))
  ;; intendation
  (setq-local tab-stop-list gpl99-field-positions)
  (setq-local indent-line-function 'asm99-indent-line)
  (setq-local indent-tabs-mode nil)
  ;; comments
  (use-local-map asm99-keymap)
  (set (make-local-variable 'comment-start) ";")
  (set (make-local-variable 'comment-padding) "")
  (set (make-local-variable 'comment-style) 'plain)
  ;; enable smart minor modes by default
  (gpl99-smart-tab-mode 1)
  (gpl99-smart-backspace-mode 1)
  ;; run user hooks
  (run-hooks 'gpl99-mode-hook))

(provide 'gpl99-mode)


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
    ( ,(regexp-opt basic99-statements 'symbols) . font-lock-keyword-face)
    ( ,(regexp-opt basic99-subprograms 'symbols) . font-lock-builtin-face)
    ( ,(regexp-opt basic99-functions 'symbols) . font-lock-function-name-face)
    ( ,(regexp-opt basic99-commands 'symbols) . font-lock-warning-face)
    ; numbers (line number references and float literals)
    ("\\<[0-9.]+\\(?:E[-+]?[0-9]+\\)?\\>" . font-lock-variable-name-face)
    ))

(defvar basic99-syntax-table
  (let ((table (make-syntax-table))
        (symbols '(?# ?@ ?\[ ?\\ ?\]))
        (punctuations '(?% ?& ?* ?+ ?- ?/ ?< ?= ?>)))
    (mapc (lambda (c) (modify-syntax-entry c "_" table)) symbols)
    (mapc (lambda (c) (modify-syntax-entry c "." table)) punctuations)
    table))

;; major and minor mode definitions

(defvar basic99-mode-hook nil)

(define-derived-mode basic99-mode prog-mode "basic99"
  "Major mode for editing TI BASIC and TI Extended BASIC source files"
  (interactive)
  ;; syntax highlighting
  (set-syntax-table basic99-syntax-table)
  (setq-local font-lock-defaults (list basic99-font-lock-keywords t t))
  ;; indentation
  (setq-local indent-tabs-mode nil)
  ;; run user hooks
  (run-hooks 'basic99-mode-hook))

(provide 'basic99-mode)


;;; Optional key assignments (or put into .emacs)

;(global-set-key [f3] 'asm99-goto-symbol-definition)
;(global-set-key [S-f3] 'asm99-show-symbol-definition)
