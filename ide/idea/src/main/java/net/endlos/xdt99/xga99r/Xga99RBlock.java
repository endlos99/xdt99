package net.endlos.xdt99.xga99r;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xga99r.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xga99RBlock extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xga99RTypes.INSTRUCTION, Xga99RTypes.DIRECTIVE,
            Xga99RTypes.PREPROCESSOR, Xga99RTypes.UNKNOWN_MNEM);
    private final static TokenSet operators = TokenSet.create(Xga99RTypes.OP_AST, Xga99RTypes.OP_MISC);
    private final static TokenSet signs = TokenSet.create(Xga99RTypes.OP_PLUS, Xga99RTypes.OP_MINUS);
    private final static TokenSet separators = TokenSet.create(Xga99RTypes.OP_SEP, Xga99RTypes.OP_LPAREN,
            Xga99RTypes.OP_NOT);
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
        ASTNode previousChild = null;
        ASTNode child = myNode.getFirstChildNode();
        while (child != null) {
            if (child.getElementType() == Xga99RTypes.CRLF) {
                blocks.add(new Xga99RBlock(child, previousChild));
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0) {  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xga99RBlock(child, previousChild));
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
                    // whitespace <-> comment: line comment, leave untouched
                    return null;
                } else if (e instanceof Xga99RInstruction || e instanceof Xga99RDirective ||
                        e instanceof Xga99RPreprocessor) {
                    // instruction <-> comment (with or without operands)
                    int diffLength = getPadDiffWithinInstruction(e);  // anticipated padding change within instruction
                    return pad(Xga99RCodeStyleSettings.XGA99_COMMENT_TAB_STOP -
                                    Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP,
                            left.getTextLength() + diffLength);  // comment after instruction
                } else {
                    // label <-> comment
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
            // separator <-> operand
            else if (leftToken == Xga99RTypes.OP_SEP) {
                return fix(1);
            }
            // operand <-> separator
            else if (rightToken == Xga99RTypes.OP_SEP) {
                return fix(0);
            }
            // parens <-> *
            else if (leftToken == Xga99RTypes.OP_LPAREN || rightToken == Xga99RTypes.OP_RPAREN) {
                return fix(0);
            }
            // * <-> +/- signs and operators <-> *
            else if (signs.contains(leftToken)) {
                // no matter what right is, is left sign or operator?
                return fix(isTokenSign(left) ? 0 : 1);
            }
            else if (signs.contains(rightToken)) {
                // +/- <-> +/- covered by previous if case
                return fix(1);  // operator
            }
            else if (leftToken == Xga99RTypes.OP_NOT) {
                return fix(0);  // unary ~ is not ambiguous
            }
            // * <-> operator <-> * but register and local label, and vice versa
            else if (operators.contains(rightToken)) {
                return fix(1);
            }
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

    private int getPadDiffWithinInstruction(PsiElement instruction) {
        if (instruction.getChildren().length == 0)  // doesn't include mnemonic token
            return 0;
        // instruction parts
        int mnemonicLength = instruction.getFirstChild().getTextLength();
        int operandsLength = instruction.getLastChild().getTextLength();
        // operands
        int opsSpaceLength = 0;
        int opsSpaceCount = 0;
        PsiElement arg = instruction.getLastChild().getFirstChild();
        PsiElement prev = null;
        while (arg != null) {
            if (arg instanceof PsiWhiteSpace) {
                // count current spaces
                opsSpaceLength += arg.getTextLength();
                arg = arg.getNextSibling();
                continue;
            }
            // compute desired spaces (re-implementation of Block logic above)
            IElementType argToken = arg.getNode().getElementType();
            PsiElement next = arg.getNextSibling();
            if (next instanceof PsiWhiteSpace) {
                next = next.getNextSibling();  // never two PsiWhiteSpace in a row
            }
            if (signs.contains(argToken)) {
                if (!isTokenSign(arg.getNode()))
                    opsSpaceCount += 2;
            } else if (operators.contains(argToken)) {
                if (prev != null)
                    ++opsSpaceCount;  // before operator
                if (next != null && !Xga99RUtil.isLocalLabelExpr(next))
                    ++opsSpaceCount;  // after operator
            } else if (argToken == Xga99RTypes.OP_SEP) {
                ++opsSpaceCount;  // after operator
            }
            // no spacing with parens, as no space on one side, and operator on other
            prev = arg;
            arg = arg.getNextSibling();
        }
        // compute spacing diff, within instruction(!)
        int currentSpaces = instruction.getTextLength() - mnemonicLength - (operandsLength - opsSpaceLength);
        int targetSpaces = (Xga99RCodeStyleSettings.XGA99_OPERANDS_TAB_STOP -
                Xga99RCodeStyleSettings.XGA99_MNEMONIC_TAB_STOP - mnemonicLength) +  // mnemonic spaces
                opsSpaceCount;  // operands spaces
        return targetSpaces - currentSpaces;  // can be negative
    }

    private boolean isTokenSign(ASTNode node) {
        // +/- is a sign if to the left there is ...
        // - nothing
        // - another +/-
        // - a ~
        // - any other operator
        ASTNode left = node.getTreePrev();
        if (left instanceof PsiWhiteSpace)
            left = left.getTreePrev();  // skip whitespace
        if (left == null)
            return true;
        IElementType leftToken = left.getElementType();
        return separators.contains(leftToken) || signs.contains(leftToken) || operators.contains(leftToken);
    }

}
