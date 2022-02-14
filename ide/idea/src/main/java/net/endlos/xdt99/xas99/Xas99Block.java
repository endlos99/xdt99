package net.endlos.xdt99.xas99;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiComment;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiWhiteSpace;
import com.intellij.psi.TokenType;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.psi.*;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Block extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xas99Types.INSTRUCTION, Xas99Types.DIRECTIVE,
            Xas99Types.PREPROCESSOR, Xas99Types.UNKNOWN_MNEM);
    private final static TokenSet operators = TokenSet.create(Xas99Types.OP_AST, Xas99Types.OP_MISC);
    private final static TokenSet signs = TokenSet.create(Xas99Types.OP_PLUS, Xas99Types.OP_MINUS);
    private final static TokenSet modifiers = TokenSet.create(Xas99Types.MOD_AUTO, Xas99Types.MOD_LEN,
            Xas99Types.MOD_XBANK);
    private final static TokenSet separators = TokenSet.create(Xas99Types.OP_SEP, Xas99Types.OP_LPAREN,
            Xas99Types.OP_NOT);
    private final ASTNode myPreviousNode;

    public Xas99Block(@NotNull ASTNode node) {
        super(node, null, null);
        myPreviousNode = null;
    }

    protected Xas99Block(@NotNull ASTNode node, @Nullable ASTNode prevNode) {
        super(node, null, null);
        myPreviousNode = prevNode;
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<Block>();
        ASTNode previousChild = null;
        ASTNode child = myNode.getFirstChildNode();
        while (child != null) {
            if (child.getElementType() == Xas99Types.CRLF) {
                blocks.add(new Xas99Block(child, previousChild));
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0) {  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xas99Block(child, previousChild));
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
        if (statements.contains(t) || t == Xas99Types.COMMENT) {
            return Indent.getNormalIndent();
        }
        return Indent.getNoneIndent();
    }

    @Nullable
    @Override
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xas99Block && child2 instanceof Xas99Block) {
            ASTNode left = ((Xas99Block) child1).getNode();
            IElementType leftToken = left.getElementType();
            ASTNode right = ((Xas99Block) child2).getNode();
            IElementType rightToken = right.getElementType();
            // label <-> mnemonic
            if (leftToken == Xas99Types.LABELDEF && statements.contains(rightToken)) {
                return pad(Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1, left.getTextLength());
            }
            // whitespace <-> mnemonic
            else if (leftToken == Xas99Types.CRLF && statements.contains(rightToken)) {
                return pad(Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - 1, 0);
            }
            // mnemonic <-> operands
            // NOTE: we don't want to list all mnemonic tokens here
            else if (statements.contains(this.getNode().getElementType()) &&
                    ((Xas99Block) child1).myPreviousNode == null && !(right.getPsi() instanceof PsiComment)) {
                return pad(Xas99CodeStyleSettings.XAS99_OPERANDS_TAB_STOP - Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // * <-> comments
            else if (rightToken == Xas99Types.COMMENT) {
                PsiElement e = left.getPsi();
                if (left.getElementType() == Xas99Types.CRLF) {
                    // whitespace <-> comment: line comment, leave untouched
                    return null;
                } else if (e instanceof Xas99Instruction || e instanceof Xas99Directive ||
                        e instanceof Xas99Preprocessor) {
                    // instruction <-> comment (with or without operands)
                    int diffLength = getPadDiffWithinInstruction(e);  // anticipated padding change within instruction
                    return pad(Xas99CodeStyleSettings.XAS99_COMMENT_TAB_STOP -
                                    Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP,
                            left.getTextLength() + diffLength);  // comment after instruction
                } else {
                    // label <-> comment
                    int extraLength = 0;
                    if (left.getElementType() == Xas99Types.OP_COLON) {
                        // add Labeldef length if continuation label
                        PsiElement pe = left.getPsi().getPrevSibling();
                        if (pe instanceof Xas99Labeldef)
                            extraLength = pe.getTextLength();
                    }
                    return pad(Xas99CodeStyleSettings.XAS99_COMMENT_TAB_STOP - 1,  // first position is 1
                            left.getTextLength() + extraLength);  // comment after label only
                }
            }
            // separator <-> operand
            else if (leftToken == Xas99Types.OP_SEP) {
                return fix(Xas99CodeStyleSettings.XAS99_STRICT ? 0 : 1);
            }
            // operand <-> separator
            else if (rightToken == Xas99Types.OP_SEP) {
                return fix(0);
            }
            // modifier
            else if (modifiers.contains(leftToken)) {
                return fix(0);
            }
            // parens <-> *
            else if (leftToken == Xas99Types.OP_LPAREN || rightToken == Xas99Types.OP_RPAREN) {
                return fix(0);
            }
            // * <-> +/- signs and operators <-> *
            else if (signs.contains(leftToken)) {
                // no matter what right is, is left sign or operator?
                return fix(isTokenSign(left) ? 0 : (Xas99CodeStyleSettings.XAS99_STRICT ? 0 : 1));
            }
            else if (signs.contains(rightToken)) {
                if (leftToken == Xas99Types.OP_REGISTER)
                    return fix(0);
                // +/- <-> +/- covered by previous if case
                return fix(Xas99CodeStyleSettings.XAS99_STRICT ? 0 : 1);  // operator
            }
            else if (leftToken == Xas99Types.OP_NOT) {
                return fix(0);  // unary ~ is not ambiguous
            }
            // * <-> operator <-> * but register and local label, and vice versa
            else if (operators.contains(rightToken)) {
                return fix(Xas99CodeStyleSettings.XAS99_STRICT ? 0 : 1);
            }
            else if (operators.contains(leftToken) && rightToken != Xas99Types.OP_REGISTER &&
                    !Xas99Util.isLocalLabelExpr(right.getPsi())) {
                return fix(Xas99CodeStyleSettings.XAS99_STRICT ? 0 : 1);
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
                if (prev != null && prev.getNode().getElementType() != Xas99Types.OP_REGISTER)
                    ++opsSpaceCount;  // before operator
                if (next != null && (next.getNode().getElementType() != Xas99Types.OP_REGISTER &&
                        !Xas99Util.isLocalLabelExpr(next)))
                    ++opsSpaceCount;  // after operator
            } else if (argToken == Xas99Types.OP_SEP) {
                ++opsSpaceCount;  // after operator
            }
            // no spacing with parens, as no space on one side, and operator on other
            prev = arg;
            arg = arg.getNextSibling();
        }
        // compute spacing diff, within instruction(!)
        int currentSpaces = instruction.getTextLength() - mnemonicLength - (operandsLength - opsSpaceLength);
        int targetSpaces = (Xas99CodeStyleSettings.XAS99_OPERANDS_TAB_STOP -
                Xas99CodeStyleSettings.XAS99_MNEMONIC_TAB_STOP - mnemonicLength) +  // mnemonic spaces
                (Xas99CodeStyleSettings.XAS99_STRICT ? 0 : opsSpaceCount);  // operands spaces
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
