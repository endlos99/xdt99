package net.endlos.xdt99.xas99;

import com.intellij.openapi.actionSystem.DataContext;
import com.intellij.openapi.actionSystem.LangDataKeys;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.editor.Caret;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.editor.EditorModificationUtil;
import com.intellij.openapi.editor.actionSystem.EditorActionHandler;
import com.intellij.openapi.editor.actionSystem.EditorWriteActionHandler;

public class Xas99EditorWriteActionHandler extends EditorWriteActionHandler {
    private final EditorActionHandler defaultHandler;
    private final String maxTabs = "                                                            ";  // 60 spaces

    public Xas99EditorWriteActionHandler(EditorActionHandler defaultHandler) {
        this.defaultHandler = defaultHandler;
    }

    public Xas99EditorWriteActionHandler(EditorActionHandler defaultHandler, boolean runForEachCaret) {
        super(runForEachCaret);
        this.defaultHandler = defaultHandler;
    }

    @Override
    public void doExecute(final Editor editor, Caret caret, DataContext dataContext) {
        if (LangDataKeys.LANGUAGE.getData(dataContext) != Xas99Language.INSTANCE) {
            defaultHandler.execute(editor, caret, dataContext);
            return;
        }

        final int column = editor.getCaretModel().getLogicalPosition().column;
        int stop;
        // column is 0-based, tab stops are 1-based
        if (column < Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_MNEMONIC_TAB_STOP - 1) {
            stop = Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_MNEMONIC_TAB_STOP - 1;
        } else if (column < Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_OPERANDS_TAB_STOP - 1) {
            stop = Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_OPERANDS_TAB_STOP - 1;
        } else if (column < Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_COMMENT_TAB_STOP - 1) {
            stop = Xas99CodeStyleSettings.getInstance(editor.getProject()).XAS99_COMMENT_TAB_STOP - 1;
        } else {
            stop = column + 4;
        }

        final String blanks = maxTabs.substring(0, stop - column);
        ApplicationManager.getApplication().runWriteAction(
                new Runnable() {
                    public void run() {
                        EditorModificationUtil.insertStringAtCaret(editor, blanks);
                    }
                }
        );
    }

}
