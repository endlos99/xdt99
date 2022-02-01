// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99r.psi.*;

public class Xga99RInstructionImpl extends ASTWrapperPsiElement implements Xga99RInstruction {

  public Xga99RInstructionImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99RVisitor visitor) {
    visitor.visitInstruction(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99RVisitor) accept((Xga99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xga99RArgsFI getArgsFI() {
    return findChildByClass(Xga99RArgsFI.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFII getArgsFII() {
    return findChildByClass(Xga99RArgsFII.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFIII getArgsFIII() {
    return findChildByClass(Xga99RArgsFIII.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFIV getArgsFIV() {
    return findChildByClass(Xga99RArgsFIV.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFIX getArgsFIX() {
    return findChildByClass(Xga99RArgsFIX.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFV getArgsFV() {
    return findChildByClass(Xga99RArgsFV.class);
  }

  @Override
  @Nullable
  public Xga99RArgsFX getArgsFX() {
    return findChildByClass(Xga99RArgsFX.class);
  }

  @Override
  @Nullable
  public Xga99RArgsI getArgsI() {
    return findChildByClass(Xga99RArgsI.class);
  }

  @Override
  @Nullable
  public Xga99RArgsII getArgsII() {
    return findChildByClass(Xga99RArgsII.class);
  }

  @Override
  @Nullable
  public Xga99RArgsIII getArgsIII() {
    return findChildByClass(Xga99RArgsIII.class);
  }

  @Override
  @Nullable
  public Xga99RArgsIX getArgsIX() {
    return findChildByClass(Xga99RArgsIX.class);
  }

  @Override
  @Nullable
  public Xga99RArgsVI getArgsVI() {
    return findChildByClass(Xga99RArgsVI.class);
  }

  @Override
  @Nullable
  public Xga99RArgsVII getArgsVII() {
    return findChildByClass(Xga99RArgsVII.class);
  }

  @Override
  @Nullable
  public Xga99RArgsVIII getArgsVIII() {
    return findChildByClass(Xga99RArgsVIII.class);
  }

}
