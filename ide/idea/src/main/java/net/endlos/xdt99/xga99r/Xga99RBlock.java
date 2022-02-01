package net.endlos.xdt99.xga99r;

import com.intellij.formatting.Block;
import com.intellij.formatting.Indent;
import com.intellij.formatting.Spacing;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.TokenType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99r.psi.Xga99RDirective;
import net.endlos.xdt99.xga99r.psi.Xga99RInstruction;
import net.endlos.xdt99.xga99r.psi.Xga99RLabeldef;
import net.endlos.xdt99.xga99r.psi.Xga99RTypes;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99RBlock extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xga99RTypes.INSTRUCTION, Xga99RTypes.DIRECTIVE,
            Xga99RTypes.PREPROCESSOR, Xga99RTypes.UNKNOWN_MNEM);
    private final static TokenSet operators = TokenSet.create(Xga99RTypes.OP_PLUS, Xga99RTypes.OP_MINUS,
            Xga99RTypes.OP_AST, Xga99RTypes.OP_MISC);
    private final ASTNode myPreviousNode;

    public Xga99RBlock(@NotNull ASTNode node) {
        super(node, null, null);
        myPreviousNode = null;
    }

    protected Xga99RBlock(@NotNull ASTNode node, @Nullable ASTNode prevNode) {
        super(node, null, null);
        myPreviousNode = prevNode;
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<>();
        ASTNode child = myNode.getFirstChildNode();
        ASTNode previousChild = null;
        while (child != null) {
            if (child.getElementType() == Xga99RTypes.CRLF) {
                blocks.add(new Xga99RBlock(child, previousChild));
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0)  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xga99RBlock(child, previousChild));
                previousChild = child;
            }
            child = child.getTreeNext();
        }
        return blocks;
    }

    @Override
    public Indent getIndent() {
        IElementType t = this.getNode().getElementType();
        if (statements.contains(t) || t == Xga99RTypes.COMMENT) {
            return Indent.getNormalIndent();
        }
        return Indent.getNoneIndent();
    }

    @Nullable
    @Override
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xga99RBlock && child2 instanceof Xga99RBlock) {
            ASTNode left = ((Xga99RBlock) child1).getNode();
            IElementType leftToken = left.getElementType();
            ASTNode right = ((Xga99RBlock) child2).getNode();
            IElementType rightToken = right.getElementType();
            // label <-> mnemonic
            if (leftToken == Xga99RTypes.LABELDEF && statements.contains(rightToken)) {
                return pad(Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1, left.getTextLength());
            }
            // whitespace <-> mnemonic
            else if (leftToken == Xga99RTypes.CRLF && statements.contains(rightToken)) {
                return pad(Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - 1, 0);
            }
            // mnemonic <-> operands
            // NOTE: we don't want to list all mnemonic tokens here
            else if (statements.contains(this.getNode().getElementType()) &&
                    ((Xga99RBlock) child1).myPreviousNode == null && !(right.getPsi() instanceof PsiComment)) {
                return pad(Xga99RCodeStyleSettings.XGA99_OPERANDS_TAB_STOP - Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // * <-> comments
            else if (rightToken == Xga99RTypes.COMMENT) {
                PsiElement e = left.getPsi();
                if (left.getElementType() == Xga99RTypes.CRLF) {
                    return null;  // comment as line comment: leave untouched
                } else if (e instanceof Xga99RInstruction || e instanceof Xga99RDirective) {
                    int extraLength = getPadWithinInstruction(e);  // extra padding between mnemonic and ops
                    return pad(Xga99RCodeStyleSettings.XGA99_COMMENT_TAB_STOP - Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP,
                            left.getTextLength() + extraLength);  // comment after instruction
                } else {
                    int extraLength = 0;
                    if (left.getElementType() == Xga99RTypes.OP_COLON) {
                        // add Labeldef length if continuation label
                        PsiElement pe = left.getPsi().getPrevSibling();
                        if (pe instanceof Xga99RLabeldef)
                            extraLength = pe.getTextLength();
                    }
                    return pad(Xga99RCodeStyleSettings.XGA99_COMMENT_TAB_STOP - 1,  // first position is 1
                            left.getTextLength() + extraLength);  // comment after label only
                }
            }
            // separator <-> argument
            else if (leftToken == Xga99RTypes.OP_SEP) {
                return fix(1);
            }
            // argument <-> separator
            else if (rightToken == Xga99RTypes.OP_SEP) {
                return fix(0);
            }
            // parens <-> *
            else if (leftToken == Xga99RTypes.OP_LPAREN || rightToken == Xga99RTypes.OP_RPAREN) {
                return fix(0);
            }
            // operator <-> * but local label, and vice versa
            else if ((operators.contains(leftToken) && !Xga99RUtil.isLocalLabelExpr(right.getPsi()))) {
                return fix(1);
            }
            // everything else remains untouched
        }
        return null;
    }

    @Override
    public boolean isLeaf() {
        return myNode.getFirstChildNode() == null;
    }

    private Spacing pad(int size, int used) {
        if (used < size)
            return Spacing.createSpacing(size - used, size - used, 0, true, 0);
        else
            return null;
    }

    private Spacing fix(int size) {
        return Spacing.createSpacing(size, size, 0, true, 0);
    }


    private int getPadWithinInstruction(PsiElement instruction) {
        if (instruction.getChildren().length == 0)  // doesn't include mnemonic token
            return 0;
        int mnemonicLength = instruction.getFirstChild().getTextLength();
        int argumentLength = instruction.getLastChild().getTextLength();
        int currentSpaces = instruction.getTextLength() - mnemonicLength - argumentLength;
        int targetSpaces = Xga99RCodeStyleSettings.XGA99_OPERANDS_TAB_STOP -
                Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - mnemonicLength;
        return targetSpaces - currentSpaces;  // can be negative
    }

}
