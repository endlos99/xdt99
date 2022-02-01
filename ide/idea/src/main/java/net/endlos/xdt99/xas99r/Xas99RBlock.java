package net.endlos.xdt99.xas99r;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99r.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99RBlock extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xas99RTypes.INSTRUCTION, Xas99RTypes.DIRECTIVE,
            Xas99RTypes.PREPROCESSOR, Xas99RTypes.UNKNOWN_MNEM);
    private final static TokenSet operators = TokenSet.create(Xas99RTypes.OP_PLUS, Xas99RTypes.OP_MINUS,
            Xas99RTypes.OP_AST, Xas99RTypes.OP_MISC);
    private final static TokenSet modifiers = TokenSet.create(Xas99RTypes.MOD_AUTO, Xas99RTypes.MOD_LEN,
            Xas99RTypes.MOD_XBANK);
    private final ASTNode myPreviousNode;

    public Xas99RBlock(@NotNull ASTNode node) {
        super(node, null, null);
        myPreviousNode = null;
    }

    protected Xas99RBlock(@NotNull ASTNode node, @Nullable ASTNode prevNode) {
        super(node, null, null);
        myPreviousNode = prevNode;
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<Block>();
        ASTNode previousChild = null;
        ASTNode child = myNode.getFirstChildNode();
        while (child != null) {
            if (child.getElementType() == Xas99RTypes.CRLF) {
                blocks.add(new Xas99RBlock(child, previousChild));
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0) {  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xas99RBlock(child, previousChild));
                }
                previousChild = child;
            }
            child = child.getTreeNext();
        }
        return blocks;
    }

    @Override
    public Indent getIndent() {
        IElementType t = this.getNode().getElementType();
        if (statements.contains(t) || t == Xas99RTypes.COMMENT) {
            return Indent.getNormalIndent();
        }
        return Indent.getNoneIndent();
    }

    @Nullable
    @Override
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xas99RBlock && child2 instanceof Xas99RBlock) {
            ASTNode left = ((Xas99RBlock) child1).getNode();
            IElementType leftToken = left.getElementType();
            ASTNode right = ((Xas99RBlock) child2).getNode();
            IElementType rightToken = right.getElementType();
            // label <-> mnemonic
            if (leftToken == Xas99RTypes.LABELDEF && statements.contains(rightToken)) {
                return pad(Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1, left.getTextLength());
            }
            // whitespace <-> mnemonic
            else if (leftToken == Xas99RTypes.CRLF && statements.contains(rightToken)) {
                return pad(Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1, 0);
            }
            // mnemonic <-> operands
            // NOTE: we don't want to list all mnemonic tokens here
            else if (statements.contains(this.getNode().getElementType()) &&
                    ((Xas99RBlock) child1).myPreviousNode == null && !(right.getPsi() instanceof PsiComment)) {
                return pad(Xas99RCodeStyleSettings.XAS99_OPERANDS_TAB_STOP - Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // * <-> comments
            else if (rightToken == Xas99RTypes.COMMENT) {
                PsiElement e = left.getPsi();
                if (left.getElementType() == Xas99RTypes.CRLF) {
                    // whitespace <-> comment: line comment, leave untouched
                    return null;
                } else if (e instanceof Xas99RInstruction || e instanceof Xas99RDirective) {
                    // instruction <-> comment (with or without operands)
                    int diffLength = getPadDiffWithinInstruction(e);  // extra padding within intruction
                    return pad(Xas99RCodeStyleSettings.XAS99_COMMENT_TAB_STOP -
                                    Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP,
                            left.getTextLength() + diffLength);  // comment after instruction
                } else {
                    // label <-> comment
                    int extraLength = 0;
                    if (left.getElementType() == Xas99RTypes.OP_COLON) {
                        // add Labeldef length if continuation label
                        PsiElement pe = left.getPsi().getPrevSibling();
                        if (pe instanceof Xas99RLabeldef)
                            extraLength = pe.getTextLength();
                    }
                    return pad(Xas99RCodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1,  // first position is 1
                            left.getTextLength() + extraLength);  // comment after label only
                }
            }
            // separator <-> operand
            else if (leftToken == Xas99RTypes.OP_SEP) {
                return fix(1);
            }
            // operand <-> separator
            else if (rightToken == Xas99RTypes.OP_SEP) {
                return fix(0);
            }
            // modifier
            else if (modifiers.contains(leftToken)) {
                return fix(0);
            }
            // parens <-> *
            else if (leftToken == Xas99RTypes.OP_LPAREN || rightToken == Xas99RTypes.OP_RPAREN) {
                return fix(0);
            }
            // operator <-> * but register and local label, and vice versa
            else if ((operators.contains(rightToken) && leftToken != Xas99RTypes.OP_REGISTER) ||
                    (operators.contains(leftToken) && rightToken != Xas99RTypes.OP_REGISTER &&
                            !Xas99RUtil.isLocalLabelExpr(right.getPsi()))) {
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
        if (used < size) {
            return Spacing.createSpacing(size - used, size - used, 0, true, 0);
        } else {
            return null;
        }
    }

    private Spacing fix(int size) {
        return Spacing.createSpacing(size, size, 0, true, 0);
    }

    private int getPadDiffWithinInstruction(PsiElement instruction) {
        if (instruction.getChildren().length == 0)  // doesn't include mnemonic token
            return 0;
        // instruction parts
        int mnemonicLength = instruction.getFirstChild().getTextLength();
        int operandsLength = instruction.getLastChild().getTextLength();
        // operands
        int opsSpaceLength = 0;
        int opsSpaceCount = 0;
        for (PsiElement arg : instruction.getLastChild().getChildren()) {
            if (arg instanceof PsiWhiteSpace) {
                opsSpaceLength += arg.getTextLength();
                ++opsSpaceCount;
            }
        }
        // compute spacing diff, within instruction(!)
        int currentSpaces = instruction.getTextLength() - mnemonicLength - operandsLength + opsSpaceLength;
        int targetSpaces = Xas99RCodeStyleSettings.XAS99_OPERANDS_TAB_STOP -
                Xas99RCodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - mnemonicLength + opsSpaceCount;
        return targetSpaces - currentSpaces;  // can be negative
    }

}
