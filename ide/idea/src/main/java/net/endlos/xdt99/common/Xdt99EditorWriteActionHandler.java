package net.endlos.xdt99.common;

import com.intellij.openapi.actionSystem.DataContext;
import com.intellij.openapi.actionSystem.LangDataKeys;
import com.intellij.openapi.application.ApplicationManager;
import com.intellij.openapi.editor.Caret;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.editor.EditorModificationUtil;
import com.intellij.openapi.editor.actionSystem.EditorActionHandler;
import com.intellij.openapi.editor.actionSystem.EditorWriteActionHandler;
import net.endlos.xdt99.xas99.Xas99CodeStyleSettings;
import net.endlos.xdt99.xas99.Xas99Language;
import net.endlos.xdt99.xas99r.Xas99RCodeStyleSettings;
import net.endlos.xdt99.xas99r.Xas99RLanguage;
import net.endlos.xdt99.xga99.Xga99CodeStyleSettings;
import net.endlos.xdt99.xga99.Xga99Language;
import net.endlos.xdt99.xga99r.Xga99RCodeStyleSettings;
import net.endlos.xdt99.xga99r.Xga99RLanguage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

public class Xdt99EditorWriteActionHandler extends EditorWriteActionHandler {
    private final EditorActionHandler defaultHandler;
    private final String maxTabs = "                                                            ";  // 60 spaces

    public Xdt99EditorWriteActionHandler(EditorActionHandler defaultHandler) {
        this.defaultHandler = defaultHandler;
    }

    public Xdt99EditorWriteActionHandler(EditorActionHandler defaultHandler, boolean runForEachCaret) {
        super(runForEachCaret);
        this.defaultHandler = defaultHandler;
    }

    @Override
    public void doExecute(@NotNull final Editor editor, @Nullable final Caret caret, final DataContext dataContext) {
        final int column = editor.getCaretModel().getLogicalPosition().column;
        int stop;

        // column is 0-based, tab stops are 1-based
        if (LangDataKeys.LANGUAGE.getData(dataContext) == Xas99Language.INSTANCE) {
            if (column < Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1) {
                stop = Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1;
            } else if (column < Xas99CodeStyleSettings.XAS99_OPERANDS_TAB_STOP - 1) {
                stop = Xas99CodeStyleSettings.XAS99_OPERANDS_TAB_STOP - 1;
            } else if (column < Xas99CodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1) {
                stop = Xas99CodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1;
            } else {
                stop = column + 4;
            }
        } else if (LangDataKeys.LANGUAGE.getData(dataContext) == Xas99RLanguage.INSTANCE) {
            if (column < Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1) {
                stop = Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1;
            } else if (column < Xas99RCodeStyleSettings.XAS99_OPERANDS_TAB_STOP - 1) {
                stop = Xas99RCodeStyleSettings.XAS99_OPERANDS_TAB_STOP - 1;
            } else if (column < Xas99RCodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1) {
                stop = Xas99RCodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1;
            } else {
                stop = column + 4;
            }
        } else if (LangDataKeys.LANGUAGE.getData(dataContext) == Xga99Language.INSTANCE) {
            if (column < Xga99CodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1) {
                stop = Xga99CodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1;
            } else if (column < Xga99CodeStyleSettings.XGA99_OPERANDS_TAB_STOP - 1) {
                stop = Xga99CodeStyleSettings.XGA99_OPERANDS_TAB_STOP - 1;
            } else if (column < Xga99CodeStyleSettings.XGA99_COMMENT_TAB_STOP - 1) {
                stop = Xga99CodeStyleSettings.XGA99_COMMENT_TAB_STOP - 1;
            } else {
                stop = column + 4;
            }
        } else if (LangDataKeys.LANGUAGE.getData(dataContext) == Xga99RLanguage.INSTANCE) {
            if (column < Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1) {
                stop = Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1;
            } else if (column < Xga99RCodeStyleSettings.XGA99_OPERANDS_TAB_STOP - 1) {
                stop = Xga99RCodeStyleSettings.XGA99_OPERANDS_TAB_STOP - 1;
            } else if (column < Xga99RCodeStyleSettings.XGA99_COMMENT_TAB_STOP - 1) {
                stop = Xga99RCodeStyleSettings.XGA99_COMMENT_TAB_STOP - 1;
            } else {
                stop = column + 4;
            }
        } else {
            defaultHandler.execute(editor, caret, dataContext);
            return;
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
