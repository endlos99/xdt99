package net.endlos.xdt99.xas99;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.TokenType;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.formatter.common.AbstractBlock;
import com.intellij.psi.tree.IElementType;
import com.intellij.psi.tree.TokenSet;
import net.endlos.xdt99.xas99.psi.Xas99Types;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;

public class Xas99Block extends AbstractBlock {
    private final static TokenSet statements = TokenSet.create(Xas99Types.INSTRUCTION, Xas99Types.DIRECTIVE,
            Xas99Types.PREPROCESSOR, Xas99Types.UNKNOWN_MNEM);
//    private final static TokenSet operators = TokenSet.create(Xas99Types.OP_PLUS, Xas99Types.OP_MINUS,
//            Xas99Types.OP_AST, Xas99Types.OP_MISC);

    private final ASTNode myPreviousNode;
    private final Xas99CodeStyleSettings mySettings;

    public Xas99Block(@NotNull ASTNode node, CodeStyleSettings settings) {
        super(node, null, null);
        myPreviousNode = null;
        mySettings = settings.getCustomSettings(Xas99CodeStyleSettings.class);
    }

    protected Xas99Block(@NotNull ASTNode node, @Nullable ASTNode prevNode, Xas99CodeStyleSettings settings) {
        super(node, null, null);
        myPreviousNode = prevNode;
        mySettings = settings;
    }

    @Override
    protected List<Block> buildChildren() {
        List<Block> blocks = new ArrayList<Block>();
        ASTNode child = myNode.getFirstChildNode();
        ASTNode previousChild = null;
        while (child != null) {
            if (child.getElementType() == Xas99Types.CRLF) {
                previousChild = null;
            } else if (child.getElementType() != TokenType.WHITE_SPACE) {
                if (child.getTextLength() > 0)  // mostly required for potentially empty PsiErrorElement nodes
                    blocks.add(new Xas99Block(child, previousChild, mySettings));
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
            return Indent.getSpaceIndent(mySettings.XAS99_MNEMONIC_TAB_STOP - 1);
        }
        return Indent.getNoneIndent();
    }

    @Nullable
    @Override
    public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
        if (child1 instanceof Xas99Block && child2 instanceof Xas99Block) {
            ASTNode left = ((Xas99Block) child1).getNode();
            ASTNode right = ((Xas99Block) child2).getNode();
            // label <-> mnemonic
            if (left.getElementType() == Xas99Types.LABELDEF && statements.contains(right.getElementType())) {
                return pad(mySettings.XAS99_MNEMONIC_TAB_STOP - 1, left.getTextLength());
            }
            // mnemonic <-> operands
            else if (statements.contains(this.getNode().getElementType()) &&
                    ((Xas99Block) child1).myPreviousNode == null) {
                return pad(mySettings.XAS99_OPERANDS_TAB_STOP - mySettings.XAS99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // * <-> comments
            // TODO: Needs to be applied twice if separator spacing changed
            else if (right.getElementType() == Xas99Types.COMMENT &&
                    ((Xas99Block) child2).myPreviousNode != null) {
                return pad(mySettings.XAS99_COMMENT_TAB_STOP - mySettings.XAS99_MNEMONIC_TAB_STOP,
                        left.getTextLength());
            }
            // separator <-> argument
            else if (left.getElementType() == Xas99Types.OP_SEP) {
                return fix(mySettings.XAS99_RELAXED ? 1 : 0);
            }
            // argument <-> separator
            else if (right.getElementType() == Xas99Types.OP_SEP) {
                return fix(0);
            }
            // operator <-> operand and vice versa
            /* NOTE: disabled, since we cannot tell A+B from @A+B, -1 from A-1 for now
            else if (operators.contains(left.getElementType()) && right.getElementType() != Xas99Types.OP_REGISTER ||
                    operators.contains(right.getElementType()) && left.getElementType() != Xas99Types.OP_REGISTER) {
                return fix(mySettings.XAS99_RELAXED ? 1 : 0);
            }
            */
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
}
